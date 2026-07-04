import { useState } from 'react';
import { useForm } from 'react-hook-form';
export default function User() {

    const { register, handleSubmit, formState: { errors } } = useForm();
    const [loader, setLoader] = useState(true);
    const [respuesta, setRespuesa] = useState({});

    const manageSend = async (data) => {
        setLoader(false);

        const dataSend = {
            "session_id": "1234",
            "name_user": data.name_user,
            "last_name": data.last_name,
            "age": parseInt(data.age, 10)
        }
        try {
            const response = await fetch('http://localhost:5000/user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataSend)
            });
            if (response.ok) {
                const data = await response.json();
                const repuestaM = data['mensaje']
                setRespuesa(repuestaM)
                alert('los datos han sido correctamente enviados');
            }
        } catch (error) {
            console.log(`Error ${error}`);
        } finally {
            setLoader(true);
        }
    }

    return (
        <>
            <form onSubmit={handleSubmit(manageSend)}>
                <input
                    {...register('name_user', {
                        required: ' el nombre es obligatorio..',

                    })}
                    type='text'
                    placeholder='Nombre'
                    disable={!loader} />
                <input
                    {...register('last_name', {
                        required: 'el apellido es obligatorio'
                    })}
                    type='text'
                    placeholder='apellido'
                    disable={!loader}
                />
                <input
                    {...register('age', {
                        required: ' se necesita la edad...'
                    })}
                    type='text'
                    placeholder='edad..'
                    disabled={!loader} />
                {errors.age && <p>{errors.age.message}</p>}
                <button type="submit" disabled={!loader}>
                    Enviar
                </button>
            </form>
            {respuesta && (<div style={{ marginTop: '20px', padding: '15px', background: '#f0f0f0', borderRadius: '5px' }}>
                <strong>respuesta:</strong>
                <p>{respuesta.name_user} y su edad es {respuesta['age']}</p>
            </div>)}
        </>
    );
}


