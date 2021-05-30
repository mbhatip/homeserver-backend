import React, { useEffect, useState } from 'react'
import Table from './Table'
//import Form from './Form'

function App() {

    const [status, setStatus] = useState({'status': 'loading...'})
    const [isLoading, setLoading] = useState(false)
    useEffect(() => {
        async function getStatus() {
            const res = await fetch("https://memohat.xyz/api/status");
            setStatus(await res.json())
            setLoading(false)
        }
        getStatus()
    }, [isLoading])

    return <div className="container">
        <h1>Status: {isLoading ? "Loading..." : status.status}</h1>
        <h1>Memory: {status.memory}</h1>
        <button onClick={() => setLoading(true)}>
            refresh
        </button>
        <h1>Users: {status.users.length}/20</h1>
        <Table
            users={status.users}
        />
    </div>

}

export default App