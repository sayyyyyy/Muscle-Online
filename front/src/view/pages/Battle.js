import { Link } from 'react-router-dom';
import classes from "./../../style/page/Home.module.css"
import Webcam from "react-webcam";
import { useState, useEffect ,useRef,useCallback} from 'react';


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

    useEffect(() => {
        setInterval(()=>{
            setImageSrc(webcamRef.current?.getScreenshot());
            console.log(imageSrc)
            console.log(1)
        },5000);
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