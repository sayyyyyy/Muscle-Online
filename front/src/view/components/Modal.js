import classes from "./../../style/components/Modal.module.css"

const Modal=(props)=>{

    const closeModal=()=>{//home画面のルームバトルのモーダル表示
        props.setShowModal(false);
    }

    return(
        <>
            {props.showFlag ? // showFlagがtrueだったらModalを表示する
            (<div  id="overlay" className={classes.modalContent}>
                <div id="modalContent"  className={classes.overlay}>
                    <p>This is ModalContent</p>
                    <button onClick={closeModal}>Close</button>
                </div>
            </div>
            ):  // showFlagがfalse
            (<>
            </>
            )
            }
        </>
    )
}
export default Modal;