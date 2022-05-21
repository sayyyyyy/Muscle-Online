import { Link } from 'react-router-dom';
import classes from "./../../style/page/Home.module.css"
import Webcam from "react-webcam";
import { useState, useEffect ,useRef,useCallback} from 'react';
import axios from 'axios';


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
    console.log(width);
    console.log(height);

    const webcamRef = useRef(null);
    const [imageSrc, setImageSrc] = useState("")

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
        },1000);
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