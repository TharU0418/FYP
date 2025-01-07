'use client';

import styles from '../styles/globals.css';
import MessageBubble from './MessageBubble';
import InputBox from './InputBox';
import { useState } from 'react';

interface Message {
  text: string;
  sender: 'bot' | 'user';
  options?: string[];
}

const ChatWindow2: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [context, setContext] = useState<string>('chatinit');
  const [predictedSymptoms, setPredictedSymptoms] = useState<string[]>([]);
  const [currentSymptomIndex, setCurrentSymptomIndex] = useState<number>(0);
  const [Symptoms_yes, setSymptoms_yes] = useState<string[]>([]); // State to store symptoms user says "YES" to

  const handleSendMessage = async (message: string, newContext: string = context) => {
    const newMessages = [...messages, { text: message, sender: 'user' }];
    setMessages(newMessages);
    setError(null);
    console.log('message', message);

    try {
      const res = await fetch('http://127.0.0.1:5000/getresult', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message
        })
      });

      const data = await res.json();
      console.log('data', data);
      console.log('data.predicted_symptoms', data.predicted_symptoms);
      setPredictedSymptoms(data.predicted_symptoms);
      setCurrentSymptomIndex(0); // Start from the first symptom

      setMessages([
        ...newMessages,
        { text: `Do you have ${data.predicted_symptoms[0]}?`, sender: 'bot', options: ['YES', 'NO'] },
      ]);
      setContext(newContext);

    } catch (error) {
      console.error('Error fetching chatbot response:', error);
      setError('Error fetching chatbot response. Please try again.');
    }
  };

  const handleOptionClick = async (option: string) => {
    const newMessages = [...messages, { text: option, sender: 'user' }];
    setMessages(newMessages);

    const currentSymptom = predictedSymptoms[currentSymptomIndex];
    if (option === 'YES') {
      setSymptoms_yes([...Symptoms_yes, currentSymptom]); // Save symptom if user says "YES"
    }

    if (currentSymptomIndex + 1 < predictedSymptoms.length) {
      const nextSymptom = predictedSymptoms[currentSymptomIndex + 1];
      setMessages([
        ...newMessages,
        { text: `Do you have ${nextSymptom}?`, sender: 'bot', options: ['YES', 'NO'] },
      ]);
      setCurrentSymptomIndex(currentSymptomIndex + 1);
    } else {
      setMessages([
        ...newMessages,
        { text: 'Thank you for your responses. We will display the results in a second.', sender: 'bot' },
      ]);
      console.log('Symptoms the user said YES to:', Symptoms_yes);

      try {
        console.log('Symptoms yes', Symptoms_yes);

        const disease_input =  "['weight_loss', 'high_fever', 'fatigue', 'dark_urine', 'abdominal_pain']"
        

        const res = await fetch('http://127.0.0.1:5000/gefinalresult', {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            disease_input
          })
        });

        const data = await res.json();
        console.log('data', data.result);

        setMessages([
          ...newMessages,
          { text: 'data', sender: 'bot' },
        ]);

        // Handle the received data
      } catch (error) {
        console.log(error);
      }
    }
};

  console.log('Symptoms_yes', Symptoms_yes);
  return (
    <div className='flex flex-col p-20 bg-sky-950 overflow-y-auto h-screen'>
      <div className=' p-4 overflow-x-auto' style={{height:'800px'}}>
{messages.map((msg, index) => (
        <MessageBubble key={index} text={msg.text} sender={msg.sender} options={msg.options} onOptionClick={handleOptionClick} />
      ))}
            </div>

      <InputBox onSendMessage={handleSendMessage} />
      {error && <div className={styles.error}>{error}</div>}
    </div>
  );
};

export default ChatWindow2;
