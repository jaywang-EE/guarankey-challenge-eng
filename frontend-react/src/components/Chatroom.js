import React, { Component } from 'react';


class Chatroom extends Component{

  constructor(props){
    super(props)

    this.state = {
      message:"",
      messageList:[],
      guestname:"guest_"+this.makeid(),
      username:"",
      userList:[],
      currentRoom:"",
      currentRoomId:"",
      newRoomName:"",
      roomOptions:[],
      modalOpen:false,
      roomModal:false,
      indicatorName:"",
      counter:0,
    }
   
  }


  componentDidMount(){
    
  }

  

  isTyping(){
   
  }

  
  componentWillMount() {
    this.timer = null;
  }
  
  render(){
    return (
    <div className="chatBoard">
      you code
    </div>
    );
  }
}
export default Chatroom;
