'use client';
import InputBox2 from '@/components/InputBox2'
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';


const FindSymptoms = () => {

  const [diseaes, setDiseaes] = useState([]);
  const[loading, setLoading] = useState(false);

  const router = useRouter();

  const welcomeText = ["What is your symptom ?", "Tell us how you're feeling", "Share your health concern", "Let's get to the root of the problem", "Not feeling your best?"]
  const [randomText, setRandomText] = useState('');

  useEffect(() =>{
    const randomIndex = Math.floor(Math.random() * welcomeText.length);
    setRandomText(welcomeText[randomIndex]);
  }, []);

  // 4️⃣5️⃣6️⃣

  const handleSendMessage = async (message:string) => {
    console.log('message 3️⃣ ', message)
    const transformedMessage = message.replace(/\s+/g, '_');
    console.log('transformedMessage', transformedMessage.toLowerCase())


    const res = await fetch('http://127.0.0.1:5000/get_diseases_name', {
      method: 'POST',
      headers:{
        'Content-Type' : 'application/json',
      },
      body:JSON.stringify({
        symptom_user_input:transformedMessage
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
    <div className='bg-bgColor-400 h-screen py-16'>

      <h4 className='font-bold text-5xl text-black mb-6 items-left text-left'>{randomText}</h4>

      <InputBox2 onSendMessage={handleSendMessage}/>

      {loading ? (
        <div className='bg-bgColor-300 m-6 rounded-md p-4'>
          <h5 className='font-bold text-2xl text-black mb-6 text-center mt-6'>
          Based on your symptoms, you may have one of these conditions.
          </h5>
    
          <div className='bg-bgColor-200 p-8 border-black rounded-sm border-2 ml-16 mr-16 text-center'>

            {diseaes.map((item, index) => (
              <>
              <button key={index} className='bg-white p-4 text-xl rounded-xl mr-8 hover:bg-slate-400' onClick={() => handleNextPage(item)}>
              {item}
            </button>
              </>
            ))}

          </div>

          <h5 className='font-bold text-2xl text-black mb-6 text-center mt-6'>
           To get a more accurate diagnosis, we recommend to click on a illness.
          </h5>

        </div>) 
      : (<>
      </>)}
    

    </div>
  )
}

export default FindSymptoms