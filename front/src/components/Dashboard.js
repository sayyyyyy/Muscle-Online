import React from 'react'

export default function Dashboard(props) {
    return (
        <div>
            <h1>Dashboard</h1>
            <h2>ログイン状態: {props.loggedInStatus}</h2>
        </div>
    )
}