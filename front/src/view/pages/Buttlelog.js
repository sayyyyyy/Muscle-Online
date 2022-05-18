import Footer from "./../components/Footer"
import { useEffect } from "react"
import axios from "axios"

const Battlelog=(props)=>{

    useEffect(()=>{
        const gethistory=async()=>{
            const res =await axios.post("http://localhost:5001/history",
            {
                user_token:props.token,
            }
            ).then(res=>{
                console.log(1)
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
            
            <Footer />
        </>
    )
}

export default Battlelog;
