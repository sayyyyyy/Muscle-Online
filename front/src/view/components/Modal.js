import classes from "./../../style/components/Modal.module.css"
import {useState} from "react"

const Modal=(props)=>{

    const [JoinRoom,setJoinRoom]=useState(true)
    const [roomId,setRoomId]=useState("")
    const [roomPass,setRoomPass]=useState("")

    const handleSubmit=()=>{ //作成

    }

    const closeModal=()=>{//home画面のルームバトルのモーダル表示
        props.setShowModal(false);
    }

    const changeMakeRoom=()=>{//ルームの作成ボタンを押した場合
        setJoinRoom(false);
    }

    const changeJoinRoom=()=>{//ルームの参加ボタンを押した場合
        setJoinRoom(true);
    }

    return(
        <>
            {props.showFlag ? // showFlagがtrueだったらModalを表示する
            (<div  id="overlay" className={classes.overlay}>
                <div id="modalContent"  className={classes.modalContent}>
                    
                    <div>
                        <button onClick={changeJoinRoom}>ルームに参加</button> /
                        <button onClick={changeMakeRoom}>ルームの作成</button>
                        <button onClick={closeModal}>×</button>
                    </div>
                    <hr className={classes.hr}/>
                    {JoinRoom === true?
                     //ルームに参加する画面
                    (
                        <div>
                            <form onSubmit={handleSubmit}>
                                <h5>ルームの名前</h5>
                                <input 
                                  type="roomid" 
                                  name="roomid" 
                                  value={roomId} 
                                  onChange={event=> setRoomId(event.target.value)}
                                />
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
                            ルームの作成
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