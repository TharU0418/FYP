'use client';
import InputBox2 from '@/components/InputBox2'
import { PlaceholdersAndVanishInput } from '@/components/ui/placeholders-and-vanish-input';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';


const FindSymptoms = () => {

  const[loading, setLoading] = useState(false);

  const[message, setMessage] = useState('');
  const[symptom, setSymptom] = useState('');
  const[diseases, setDiseases] = useState([]); // Added disease state


  const router = useRouter();

  const welcomeText = ["What is your symptom ?", "Tell us how you're feeling", "Share your health concern", "Let's get to the root of the problem", "Not feeling your best?"]
  const [randomText, setRandomText] = useState('');

  useEffect(() =>{
    const randomIndex = Math.floor(Math.random() * welcomeText.length);
    setRandomText(welcomeText[randomIndex]);
  }, []);

  // 4️⃣5️⃣6️⃣

  const placeholders = [
    "My sore throat is making it really uncomfortable to eat or drink anything.",
    "Who is Tyler Durden?",
    "I can’t seem to get warm, no matter how many blankets I use to cover myself.",
    "I keep sneezing uncontrollably, and it feels like it’s never going to stop.",
    "My throat feels dry and scratchy, which makes me cough uncontrollably.",
  ];
 

  const getSentence = async () => {
  //  e.preventDefault(); // Prevent form submission
    console.log('message', message);
  };

  const getSymptom = async (e) => {
    e.preventDefault();

    getSentence();

    const res= await fetch('http://127.0.0.1:5000/get_sentence', {
      method : 'POST',
      headers : {
        'Content-Type' : 'application/json',
      },
      body : JSON.stringify({
        sentence : message
      }),
    });
    const data = await res.json();
    console.log('data  1️⃣', data)

    setSymptom(data.symptom)

    console.log('symptom 2️⃣', symptom)

    const transformedMessage = data.symptom.replace(/\s+/g, '_').toLowerCase();

    console.log('transformedMessage 3️⃣', transformedMessage)

    const res2 = await fetch('http://127.0.0.1:5000/get_diseases_name', {
      method: 'POST',
      headers:{
        'Content-Type' : 'application/json',
      },
      body:JSON.stringify({
        symptom_user_input:transformedMessage
      })
    })

    const data2 = await res2.json();
    console.log('data 4️⃣', data2)
   // Store diseases in the state
   setDiseases(data2.diseases);

   // Log the diseases (optional)
   console.log('Diseases:', diseases);

    const details = data2.diseases.reduce((acc: Record<string, boolean>, disease: string) => {
         acc[disease] = true;
         return acc;
       }, {});
  
      localStorage.setItem('details', JSON.stringify(details));
      setLoading(true)

  }

  useEffect(() => {
    console.log('Updated diseases:', diseases);
    setDiseases(diseases);
  }, [diseases]);


  const handleNextPage = (item: string) => {
    router.push(`/my-symptoms?disease=${encodeURIComponent(item)}`);
  };

  
  return (
    <div className='bg-bgColor-400 h-screen py-16'>

      <h4 className='font-bold text-3xl text-black mb-6 items-center text-center'>{randomText}</h4>

      {/* <InputBox2 onSendMessage={handleSendMessage}/> */}


      {/* <div className="flex"> */}
      {/* <form className="flex flex-row p-6 mt-auto w-full">
        <div className='w-10/12 border-none'>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-4 rounded-s w-full bg-white text-black"
          />

        </div>
        <div className='border-none'>
        <button
        type="submit"
        className="p-4 bg-blue-500 text-white rounded-r"
        onClick={getSymptom}
      >
        Submit
        </button>
        </div>
      </form> */}
      <PlaceholdersAndVanishInput
        placeholders={placeholders}
       // onChange={handleChange}
       onChange={(e) => setMessage(e.target.value)}
        //onSubmit={onSubmit}
        onSubmit={getSymptom}
        
      />
    {/* </div> */}

    {loading ? (
        <div className='bg-bgColor-300 m-12 mt-20 rounded-md p-4'>
          <h5 className='font-bold text-2xl text-black mb-6 text-center mt-6'>
          Based on your symptoms, you may have one of these conditions.
          </h5>
    
          <div className='bg-bgColor-200 p-8 border-black rounded-sm border-2 ml-16 mr-16 text-center'>

            {diseases.map((item, index) => (
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