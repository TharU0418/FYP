'use client';
import MessageBubble from '@/components/MessageBubble';
import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

interface Message {
    text: string,
    sender: 'bot' | 'user',
    options?: string[]
}

const NextPage = () => {

  const searchParams = useSearchParams();
  const disease = searchParams.get('disease');

  const [messages, setMessages] = useState<Message[]>([]);
  const [context, setContext] = useState<string>('chatinit');
  const [symptoms, setSymptoms] = useState<string[]>([]);
  const [currentSymptomIndex, setCurrentSymptomIndex] = useState<number>(0);
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);

  const [result, setResult] = useState<string>();

  const router = useRouter();

  const handleSubmit = async () => {
    const newMessages = [...messages, { text: disease, sender: 'user' }];
    setMessages(newMessages);

    const res = await fetch('http://127.0.0.1:5000/get_illess_name', {
      method: 'POST',
      headers: {
        'Content-Type': "application/json"
      },
      body: JSON.stringify({
        diseases_input: disease
      }),
    });

    const data = await res.json();
    setSymptoms(data.symptoms);

    setCurrentSymptomIndex(0);

    setMessages([
        ...newMessages,
        { text: `Do you have this symptom? ${data.symptoms[0]}`, sender: 'bot', options: ['Yes', 'No'] },
    ]);

  }

  // useEffect to run handleSubmit only once when the component mounts
  useEffect(() => {
    handleSubmit();
  }, []); // Empty dependency array ensures this runs only once

  const handleOptionClick = (option: string) => {
    const currentSymptom = symptoms[currentSymptomIndex];
    let updatedSymptoms = [...selectedSymptoms];

    if (option === 'Yes') {
        updatedSymptoms = [...selectedSymptoms, currentSymptom];
        setSelectedSymptoms(updatedSymptoms);
    }

    const nextIndex = currentSymptomIndex + 1;

    if (nextIndex < symptoms.length) {
        setCurrentSymptomIndex(nextIndex);
        setMessages([
            ...messages,
            { text: `Do you have this symptom? ${symptoms[nextIndex]}`, sender: 'bot', options: ['Yes', 'No'] },
        ]);
    } else {
        const transformedSymptoms = updatedSymptoms.map(symptom => symptom.replace(/_/g, " ").trim());

        setMessages([
            ...messages,
            { text: `You have selected the following symptoms: ${transformedSymptoms.join(', ')}`, sender: 'bot' },
        ]);

        finadDiseaes(transformedSymptoms);
    }
  }
  

  const finadDiseaes = async(transformedSymptoms: string[]) => {
    const res = await fetch('http://127.0.0.1:5000/predictthediseases', {
      method : 'POST',
      headers: {
        'Content-Type' : 'application/json',
      },
      body: JSON.stringify({
        symptoms: transformedSymptoms
      })
    });
    console.log('transformedSymptoms', transformedSymptoms)

    const data = await res.json();
    console.log('data', data)
    setResult(data.result); // Assuming data.result contains the result
    console.log('result', data.result)
   //handleResultPage(data.result);
  }

  const handleResultPage = (result: string) => {
    router.push(`/results?result=${result}`);
  }

  return (
    <div>
      <h1 className='text-3xl font-bold text-center mt-8'>Details for: {disease}</h1>
      {/* Add further content based on the disease */}
      {messages.map((msg, index) => (
        <MessageBubble
          key={index}
          text={msg.text}
          sender={msg.sender}
          options={msg.options}
          onOptionClick={handleOptionClick}
        />
      ))}
    </div>
  );
}

export default NextPage;
