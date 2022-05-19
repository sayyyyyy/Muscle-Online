import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import classes from './../../style/page/Loading.module.css'

const images = [
  process.env.PUBLIC_URL + "/img/image1.png",
  process.env.PUBLIC_URL + "/img/image2.png",
  process.env.PUBLIC_URL + "/img/image3.png",
  process.env.PUBLIC_URL + "/img/image4.png",
  process.env.PUBLIC_URL + "/img/image5.png",
];

const Loading=()=>{

    const settings = {
      dots: true,
      infinite: true,
      speed: 1000,
      slidesToShow: 1,
      slidesToScroll: 1
    };
    
    return(
        <>
            <div className={classes.telopContainer}>
                <p className={classes.telopText}>画面を横にしてお待ちください</p>
            </div>
            <Slider {...settings}>
              <div >
                <img src={`${process.env.PUBLIC_URL}/img/image1.png`} alt="a" className={classes.img}/>
              </div>
              <div>
               <img src={`${process.env.PUBLIC_URL}/img/image2.png`} alt="a" className={classes.img}/>
              </div>
              <div>
                <img src={`${process.env.PUBLIC_URL}/img/image3.png`} alt="a" className={classes.img}/>
              </div>
              <div>
               <img src={`${process.env.PUBLIC_URL}/img/image4.png`} alt="a" className={classes.img}/>
              </div>
              <div>
               <img src={`${process.env.PUBLIC_URL}/img/image5.png`} alt="a" className={classes.img}/>
              </div>
            </Slider>
            <div className={classes.footerContainer}>
            </div>
        </>
    )
}

export default Loading;