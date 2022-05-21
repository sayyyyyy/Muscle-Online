import { Link } from 'react-router-dom';
import classes from "./../../style/page/Home.module.css"
import Webcam from "react-webcam";
import { useState, useEffect ,useRef,useCallback} from 'react';
import axios from 'axios';
import io from "socket.io-client"
//画面の大きさを取得
export const useWindowDimensions = () => {
  const getWindowDimensions = () => {
    const { innerWidth: width, innerHeight: height } = window;
    return {
      width,
      height
    };
  }

  const [windowDimensions, setWindowDimensions] = useState(getWindowDimensions());
  useEffect(() => {
    const onResize = () => {
      setWindowDimensions(getWindowDimensions());
    }
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []);
  return windowDimensions;
}


//メインメソッド
const Battle=()=>{

    const { width, height } = useWindowDimensions();
    const videoConstraints = {
        width: width*0.9,
        height: height*0.9,
        facingMode: "user"
    };

    const webcamRef = useRef(null);
    const [imageSrc, setImageSrc] = useState("")

    const socket = io('http://localhost:5001/room');
  
    socket.on('count', (data)=>{
        console.log(data);
        console.log(5);
    });

       
    socket.on('start', function(data) {
        console.log(2);
        console.log(data);
    });

    //リアルタイム映像を画像に変換し,flaskに送る処理
    useEffect((event) => {
        setInterval(()=>{
            setImageSrc(webcamRef.current?.getScreenshot());
            axios.post("http://localhost:5001/test",
            {
                data:imageSrc
            },
            // { withCredentials: true } //cookieを含むか
            ).then(res=>{ //ユーザー作成成功
                console.log("成功")
                console.log(res)
            }).catch(err=>{//ユーザー作成失敗
                console.log("registration res", err)
            })
            event.preventDefault()
        },10000000);
    }, [imageSrc]);


    
    return (
        <>
            <Webcam
                audio={false}
                screenshotFormat="image/jpeg"
                videoConstraints={videoConstraints}
                ref={webcamRef}
            />
            
            <br/>
            <div>
            <img src={imageSrc} alt="Screenshot" />
          </div>
            
            <button >
                <Link to="/finishbattle">対戦結果</Link>
            </button>
        </>
    )
}

export default Battle;