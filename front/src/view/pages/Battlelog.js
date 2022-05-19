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
                console.log(1)
                console.log(2)
                setUserlog(res.data.data.user_data)
                console.log(3)
                console.log(userlog)
                console.log(res)
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
