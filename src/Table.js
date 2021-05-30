import React from 'react'

function TableHeader() {
    return (
        <thead>
            <tr>
                <th>Username</th>
                <th>Avatar</th>
            </tr>
        </thead>
    )
}

function TableBody(props) {
    return (
        <tbody>
            {
                props.users.map((user, index) => {
                    return (
                        <tr key={index}>
                            <td>{user['username']}</td>
                            <td><img src={"https://www.mc-heads.net/avatar/" + user['uuid']}
                            alt={user['username'] + " avatar"}
                            width="100" height="100"></img></td>
                        </tr>
                    )
                })
            }
        </tbody>
    )
}

function Table(props){
    if (!props.users) {
        return null
    }
    return (
        <table>
            <TableHeader />
            <TableBody
                users={props.users}
            />
        </table>
    )
}

export default Table