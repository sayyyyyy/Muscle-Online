import classes from "./../../style/components/Modal.module.css"
import {useState} from "react"
import axios from "axios"
import { useNavigate } from 'react-router-dom';
import io from "socket.io-client";

const Modal=(props)=>{

    //モーダルの画面遷移
    const [modalChange,setModalChange]=useState(true)

    const [roomPass,setRoomPass]=useState("")
    const [roomName,setRoomName]=useState("")

    
    const navigate=useNavigate()

    //ルームの参加ボタン
    const joinRoomButton=(event)=>{ 
        axios.post("http://localhost:5001/search_room",
        {
            room_pass:roomPass,
            user_token:props.token
        },
        // { withCredentials: true } //cookieを含むか
        ).then(res=>{ //ユーザー作成成功
            if (res.data.code===1){
                const socket = io('http://localhost:5001/room');
                socket.on('connect', function() {
                    let room_pass = roomPass;
                    let user_token = props.token;
                    socket.emit('join', {'user_token': user_token, 'room_pass': room_pass});
                    console.log('aaa');
                });

                socket.on('return', function(data) {
                    console.log(data);
                    console.log('ルームに参加しました');
                    navigate('/loading');
                });
            }
        }).catch(err=>{//ユーザー作成失敗
            console.log("registration res", err)
            console.log("ルームに参加することができませんでした")
        })
        event.preventDefault()
    }

    //ルームの作成ボタン
    const createRoomButton=(event)=>{ 
        axios.post("http://localhost:5001/create_room",
        {
            room_name:roomName,
            user_token:props.token
        },
        // { withCredentials: true } //cookieを含むか
        ).then(res=>{ //ユーザー作成成功
            console.log(res)
            if (res.data.code===1){
                let socket = io.connect('http://localhost:5001/room');
                socket.on('connect', function() {
                    
                    const room_token = res.data.data.room_token;
                    const user_token = props.token;

                    socket.emit('join', {'user_token': user_token, 'room_token': room_token});
                    
                });

                // サーバー側から返答があったときに発火する
                // {'user_list': 現在ルームにいるユーザ一覧, 'room_token': ルームトークン}
                socket.on('return', function(data) {
                    console.log(data);
                    console.log("ルームを作成しました");
                    navigate('/loading');
                });
            }
        }).catch(err=>{//ユーザー作成失敗
            console.log("registration res", err)
            console.log("ルームを作成することができませんでした")
        })
        event.preventDefault()
    }

    
    //home画面のルームバトルのモーダル表示
    const closeModal=()=>{
        props.setShowModal(false);
    }

    //ルームの作成リンク を押した場合
    const changeCreateRoom=()=>{
        setModalChange(false);
    }
    //ルームの参加リンク を押した場合
    const changeJoinRoom=()=>{
       setModalChange(true);
    }

    return(
        <>
            {props.showFlag ? // showFlagがtrueだったらModalを表示する
            (<div  id="overlay" className={classes.overlay}>
                <div id="modalContent"  className={classes.modalContent}>
                    
                    <div>
                        <button onClick={changeJoinRoom}>ルームに参加</button> /
                        <button onClick={changeCreateRoom}>ルームの作成</button>
                        <button onClick={closeModal}>×</button>
                    </div>
                    <hr className={classes.hr}/>
                    {modalChange === true?
                     //ルームに参加する画面
                    (
                        <div>
                            <form onSubmit={joinRoomButton}>
                                <h5>ルームのパスワード</h5>
                                <input 
                                  type="password"
                                  name="password" 
                                  placeholder="パスワード"
                                  value={roomPass}
                                  onChange={event=> setRoomPass(event.target.value)}
                                />
                                <br/>
                                <button type="submit">参加</button>
                            </form>
                        </div>
                    ):
                    //ルームの作成画面
                    (
                        <div>
                           <form onSubmit={createRoomButton}>
                                <h5>ルーム名</h5>
                                <input 
                                  type="name"
                                  name="name" 
                                  placeholder="ルーム名"
                                  value={roomName}
                                  onChange={event=> setRoomName(event.target.value)}
                                />
                                <br/>
                                <button type="submit">作成</button>
                            </form>
                        </div>
                    )
                    }

                </div>
            </div>
            ):  // showFlagがfalse
            (<>
            </>
            )
            }
        </>
    )
}
export default Modal;