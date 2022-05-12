/* Register.js */
import React,{useState} from "react"
import axios from "axios";

const Registration = (props) => {

  const [email, setEmail]=useState("")
  const [password,setPassword]=useState("")
  const [passwordConfirmation, setPasswordConfirmation] = useState("")

  //APIに送信
  const handleSubmit =(event)=>{ 
    console.log(email)
    console.log(password)
    axios.post("http://localhost:5000/signup",
    {
      user:{
        email:email,
        password:password,
        password_confirmation: passwordConfirmation
      }
    },
    { withCredentials: true } //cookieを含むか
    ).then(res=>{ //ユーザー作成成功
        console.log("registration res", res)
        if(res.data.status==='create'){ //railsのAPIのdata.statasを見て判断する。
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
        <input 
          type="password" 
          name="password_confirmation" 
          placeholder="確認用パスワード" 
          value={passwordConfirmation}
          onChange={event=> setPasswordConfirmation(event.target.value)}
        />
        <button type="submit">登録</button>
      </form>
    </>
  );
};

export default Registration;