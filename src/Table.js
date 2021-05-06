import React from 'react'

function TableHeader() {
    return (
        <thead>
            <tr>
                <th>Name</th>
                <th>Job</th>
            </tr>
        </thead>
    )
}

function TableBody(props) {
    return (
        <tbody>
            {
                props.characters.map((row, index) => {
                    return (
                        <tr key={index}>
                            <td>{row['name']}</td>
                            <td>{row['job']}</td>
                            <td>
                                <button onClick={() => props.remove(index)}>Delete</button>
                            </td>
                        </tr>
                    )
                })
            }
        </tbody>
    )
}

function Table(props){
    return (
        <table>
            <TableHeader />
            <TableBody
                characters={props.characters}
                remove={props.remove}
            />
        </table>
    )
}

export default Table