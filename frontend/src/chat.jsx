import { useState, useEffect } from "react";


export default function Chat() {
    return <>
        <h1>Chat AI!</h1>
        <MessaegSend />
    </>
}


function MessaegSend() {
    const [data, setData] = useState('');
    const [loading, setLoading] = useState(false);
    const [resultAi, setResultAi] = useState('');
    const manageSend = async (e) => {
        e.preventDefault();
        setLoading(true);

        const dataSend = {
            "session_id": "1234",
            "mensaje_user": data
        };


        try {
            const response = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataSend)
            });

            if (response.ok) {
                const result = await response.json();
                const resultAI = result['respuesta IA'];
                setResultAi(resultAI);
            } else {
                alert('hubo un error');
            }
        } catch (error) {
            console.log(`Error ${error}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <form onSubmit={manageSend}>
                <input
                    type="text"
                    value={data}
                    onChange={(e) => setData(e.target.value)}
                    placeholder="Tu mensaje"
                    disabled={loading}
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Enviando...' : 'Enviar Datos'}
                </button>
            </form>
            {resultAi && (
                <div style={{ marginTop: '20px', padding: '15px', background: '#f0f0f0', borderRadius: '5px' }}>
                    <strong>IA respondió:</strong>
                    <p>{resultAi}</p>
                </div>
            )}
        </>
    );
}

