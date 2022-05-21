import { Link } from 'react-router-dom';
import classes from "./../../style/page/Home.module.css"
import Webcam from "react-webcam";
import { useState, useEffect } from 'react';

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

const Battle=()=>{
    const { width, height } = useWindowDimensions();
    const videoConstraints = {
        width: width*0.9,
        height: height*0.9,
        facingMode: "user"
    };
    console.log(width);
    console.log(height);

    
    return (
        <>
            <Webcam
                audio={false}
                screenshotFormat="image/jpeg"
                videoConstraints={videoConstraints}
            />
            <br/>
            <button >
                <Link to="/finishbattle">対戦結果</Link>
            </button>
            
            
        </>
    )
}

export default Battle;