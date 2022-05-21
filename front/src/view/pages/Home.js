import Footer from "../components/Footer";
import classes from "./../../style/page/Home.module.css"
import Modal from "./../components/Modal"
import { useState } from "react";
import useToken from './../components/useToken'

const Home=()=>{
  const { token} = useToken();
  const [showModal, setShowModal]=useState(false);

  const openModal=()=>{
    setShowModal(true);
  }

  return(
    <>
      <div className={classes.backgroundStyle1}></div>
      <div className={classes.backgroundStyle2}></div>
      <button className={classes.button} onClick={openModal}>
       <img src={`${process.env.PUBLIC_URL}/img/roombattle1.png`} alt="ルームボタン" className={classes.roomimg} />
      </button>
      <Modal showFlag={showModal} setShowModal={setShowModal} token={token}/>


      <button className={classes.ratebutton}>
       <img src={`${process.env.PUBLIC_URL}/img/rate.png`} alt="ルームボタン" className={classes.rateimg} />
      </button>

      
      <Footer />
      <img src={`${process.env.PUBLIC_URL}/img/buttom.png`} alt="ルームボタン" className={classes.buttomimg} />
    </>
  )

}

export default Home;