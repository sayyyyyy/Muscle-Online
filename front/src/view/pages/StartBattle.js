import { Link } from 'react-router-dom';
import classes from "./../../style/page/StartBattle.module.css"
import io from "socket.io-client";
import { useNavigate } from 'react-router-dom';

const StartBattle=()=>{

    const navigate=useNavigate()

    const startBattleButton=(props)=>{
        let socket = io.connect('http://localhost:5001/room');
        // const user_token = props.token;
        // const room_token = props.room_token;
        const user_token = 1
        const room_token = 2;

        console.log(user_token)
        console.log(room_token)

        if(user_token===undefined && room_token===undefined ){
            console.log("バトルに参加できません")
        }
        else{
            console.log("バトルが始まります")
            socket.emit('ready', {'user_token': user_token, 'room_token': room_token})
            navigate('/battle');
        }
    }

    return (
        <>
            <div classes={classes.background}>
                <h1>対戦準備画面</h1>
                <button className={classes.readyButton} onClick={startBattleButton}>準備完了</button>
            </div>
        </>
    )
}

export default StartBattle;