'use client';
import InputBox2 from '@/components/InputBox2'
import { useRouter } from 'next/navigation';
import { useState } from 'react';


const FindSymptoms = () => {

  const [diseaes, setDiseaes] = useState([]);
  const[loading, setLoading] = useState(false);

  const router = useRouter();

  const handleSendMessage = async (message:string) => {
    console.log('message', message)

    const res = await fetch('http://127.0.0.1:5000/get_diseases_name', {
      method: 'POST',
      headers:{
        'Content-Type' : 'application/json',
      },
      body:JSON.stringify({
        symptom_user_input:message
      })
    })

    const data = await res.json();
    console.log('data', data.diseases[0])
    setDiseaes(data.diseases)

    const details = data.diseases.reduce((acc: Record<string, boolean>, disease: string) => {
      acc[disease] = true;
      return acc;
    }, {});

    localStorage.setItem('details', JSON.stringify(details));
    console.log('diseaes', diseaes)
    setLoading(true)

  }

  // const handleNextPage = (item: string) => {
  //   router.push(`/next-chat?disease=${encodeURIComponent(item)}`);
  // };

  const handleNextPage = (item: string) => {
    router.push(`/my-symptoms?disease=${encodeURIComponent(item)}`);
  };


  return (
    <div className='bg-blue-100 h-screen py-16'>

      <h4 className='font-bold text-6xl text-black mb-6 items-center text-center'>What is your symptom ?</h4>

      <InputBox2 onSendMessage={handleSendMessage}/>

      {loading ? (<>
        <h5 className='font-bold text-2xl text-black mb-6 text-center mt-6'>
        Based on your symptom you are most likely tto have one of these ilnnese
      </h5>
    
      <div className='bg-blue-500 p-8 border-black rounded-sm border-2 ml-16 mr-16 text-center'>

          {diseaes.map((item, index) => (
            <>
            <button key={index} className='bg-white p-4 text-xl rounded-xl mr-8 hover:bg-slate-400' onClick={() => handleNextPage(item)}>
            {item}
          </button>
            </>
          ))}

      </div>

      <h5 className='font-bold text-2xl text-black mb-6 text-center mt-6'>
        If you want to clarify more plase click on a diseaes 
      </h5>
      </>) : (<>
      </>)}
    

    </div>
  )
}

export default FindSymptoms