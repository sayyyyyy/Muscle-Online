import { Link } from 'react-router-dom';
import classes from "./../../style/page/StartBattle.module.css"

const StartBattle=()=>{

    const startBattleButton=(event)=>{
        let socket = io.connect('http://localhost:5001/room');
        const user_token = props.token
        const room_token = props.room_token;

        // ボタンを準備OKに変更する

        socket.emit('ready', {'user_token': user_token, 'room_token': room_token})
    
        // カウントダウンが進むたびに発火 1秒ごとに値が入ってくる
        // {'count_down': 残り秒数}

        socket.on('count', function(data) {
            console.log(data);
        });

        // ゲームスタートするときに発火する
        // {'data': 'ゲームスタート!'}

        socket.on('start', function(data) {
            console.log(data);
        });

        // ゲームが終了した時に発火する　
        // {'your_count': ユーザの回数, 'enemy_count': 相手の回数, 'winner': 勝者の名前})
        
        socket.on('finish', function(data) {
            console.log(data);
        });
    }

    return (
        <>
            <div classes={classes.background}>
                <h1>対戦準備画面</h1>
                <button className={classes.readyButton}><Link to="/battle" className={classes.linkStyle}>準備完了</Link></button>
            </div>
        </>
    )
}

export default StartBattle;