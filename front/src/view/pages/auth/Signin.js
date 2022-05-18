/* Register.js */
import React,{useState} from "react"
import axios from "axios";
import { Link } from 'react-router-dom';

const Signin= (props) => {

  const [email, setEmail]=useState("")
  const [password,setPassword]=useState("")

  //APIに送信
  const handleSubmit =(event)=>{ 
    axios.get("http://localhost:5001/",
    ).then(res=>{ //ユーザー作成成功
        console.log("registration res", res)
       
    }).catch(err=>{//ユーザー作成失敗
        console.log("registration res", err)
    })
    event.preventDefault()
  }
  
  return (
    <>
    <h2>ログイン状態: {props.loggedInStatus}</h2>
      <h1>ログイン</h1>

      <form onSubmit={handleSubmit}>
        <input 
          type="email" 
          name="email" 
          placeholder="メールアドレス" 
          value={email} 
          onChange={event=> setEmail(event.target.value)}
        />
        <input 
          type="password"
          name="password" 
          placeholder="パスワード"
          value={password}
          onChange={event=> setPassword(event.target.value)}
        />
        <button type="submit">登録</button>
      </form>
      <button> <Link to="/">戻る</Link></button>
    </>
  );
};

export default Signin;