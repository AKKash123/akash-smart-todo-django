
import './App.css';
import React,{useState,useEffect, use} from 'react'
import axios from 'axios'
import SmartTodo from './templates/SmartTodo'
function App() {
//   const [message, setMessage]=useState("");

//   //Api callfrom here
//   useEffect(() => {
//     axios.get("http://127.0.0.1:8000/api/smart-todo")
//     .then((response) => {

//         setMessage(response.data.message)
//     })

//   },[]);

  return (
      <div>
      
        <SmartTodo/>
      </div>
  );
}

export default App;



