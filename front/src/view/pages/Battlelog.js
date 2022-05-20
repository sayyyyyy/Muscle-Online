import Footer from "../components/Footer"
import { useEffect,useState} from "react"
import axios from "axios"

const Battlelog=(props)=>{

    const [userlog,setUserlog]=useState([])



    useEffect(()=>{
        const gethistory=async()=>{
            const res =await axios.post("http://localhost:5001/history",
            {
                user_token:props.token,
            }
            ).then(res=>{
                if (res.data.code===1){
                    console.log("対戦ログを取得しました")
                    setUserlog(res.data.data.user_data)
                    console.log(res.data.data.user_data)
                }
                else{
                    console.log(res.data.data.states)
                }
            }
            ).catch(res=>{
                console.log(2)
            }
            )
        }
        gethistory()
    }, [])

    return(
        <>
            <h1>対戦履歴</h1>
            <h1>
                 {userlog.win}
                 <br/ >
                {userlog.lose}
            </h1>
            
            <Footer />
        </>
    )
}

export default Battlelog;
