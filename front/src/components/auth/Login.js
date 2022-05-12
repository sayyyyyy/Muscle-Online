/* Register.js */
import React,{useState} from "react"
import axios from "axios";

const Login= (props) => {

  const [email, setEmail]=useState("")
  const [password,setPassword]=useState("")

  //APIに送信
  const handleSubmit =(event)=>{ 
    console.log(email)
    console.log(password)
    axios.post("http://localhost:5000/login",
    {
      user:{
        email:email,
        password:password,
      }
    },
    { withCredentials: true } //cookieを含むか
    ).then(res=>{ //ユーザー作成成功
        console.log("registration res", res)
        if(res.data.logged_in){ //logged_inがtrueの時に成功
          props.handleSuccessfullAuthentication(res.data) //新規登録画面に飛ぶ(home.jsの関数)
        }
       
    }).catch(err=>{//ユーザー作成失敗
        console.log("registration res", err)
    })
    event.preventDefault()
  }
  
  return (
    <>
      <h1>新規登録</h1>

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
    </>
  );
};

export default Login;