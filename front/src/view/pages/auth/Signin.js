/* Register.js */
import React,{useState} from "react"
import axios from "axios";
import { useNavigate,Link } from 'react-router-dom';

const Signin= (props) => {

  const [email, setEmail]=useState("")
  const [password,setPassword]=useState("")
  
  const navigate=useNavigate()

  //APIに送信
  const handleSubmit =(event)=>{ 
    axios.post("http://localhost:5001/signin",
    {
      user:{
        email:email,
        password:password,
      }
    }
    ).then(res=>{ //ユーザー作成成功
        props.setToken(res.data.data.access_token)
        console.log(res.data)
        if (res.data.code===1){
          navigate('/home')
        }
    }).catch(err=>{//ユーザー作成失敗
        console.log("registration res", err)
        console.log(err.response)
        console.log(err.response.status)
        console.log(err.response.headers)
    })
    setEmail("")
    setPassword("")
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
        <button type="submit" onClick={handleSubmit}>登録</button>
      </form>
      <button> <Link to="/">戻る</Link></button>
    </>
  );
};

export default Signin;