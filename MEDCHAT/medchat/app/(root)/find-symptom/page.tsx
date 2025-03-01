'use client';
import { PlaceholdersAndVanishInput } from '@/components/ui/placeholders-and-vanish-input';
import Spline from '@splinetool/react-spline';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

const FindSymptoms = () => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [symptom, setSymptom] = useState('');
  const [diseases, setDiseases] = useState([]); // Added disease state
  const [error, setError] = useState('');

  const router = useRouter();

  const welcomeText = [
    'What is your symptom?',
    "Tell us how you're feeling",
    'Share your health concern',
    "Let's get to the root of the problem",
    'Not feeling your best?',
  ];
  const [randomText, setRandomText] = useState('');

  useEffect(() => {
    const randomIndex = Math.floor(Math.random() * welcomeText.length);
    setRandomText(welcomeText[randomIndex]);
  }, []);

  const placeholders = [
    'My sore throat is making it really uncomfortable to eat or drink anything.',
    'Who is Tyler Durden?',
    "I can’t seem to get warm, no matter how many blankets I use to cover myself.",
    "I keep sneezing uncontrollably, and it feels like it’s never going to stop.",
    'My throat feels dry and scratchy, which makes me cough uncontrollably.',
  ];

  const getSentence = async () => {
    console.log('message', message);
  };

  const getSymptom = async (e: React.FormEvent) => {
    e.preventDefault();

    getSentence();

    const res = await fetch('http://127.0.0.1:5000/get_sentence', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        sentence: message,
      }),
    });
    const data = await res.json();
    console.log('predicted symptom: ', data);

    setSymptom(data.symptom);

    const transformedMessage = data.symptom.replace(/\s+/g, '_').toLowerCase();

    const res2 = await fetch('http://127.0.0.1:5000/get_diseases_name', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        symptom_user_input: transformedMessage,
      }),
    });

    const data2 = await res2.json();
    console.log('Relevant Illnesses: ', data2);

    if (data2.message === 'Enter correct symptom') {
      setError(`Currently MEDCHAT dont support for your symptom ${transformedMessage}`);
    } else {
      setDiseases(data2.diseases);
      const details = data2.diseases.reduce(
        (acc: Record<string, boolean>, disease: string) => {
          acc[disease] = true;
          return acc;
        },
        {}
      );
      localStorage.setItem('details', JSON.stringify(details));
      setLoading(true);
    }
  };

  const handleNextPage = (item: string) => {
    router.push(`/my-symptoms?disease=${encodeURIComponent(item)}`);
  };

  // Error modal component
  const ErrorModal = ({ message, onClose }: { message: string; onClose: () => void }) => {
    return (
      <div className="fixed inset-0 flex justify-center items-center bg-black bg-opacity-50">
        <div className="bg-white p-8 rounded-md w-96 relative">
          {/* <h4 className="font-bold text-xl text-red-500">Error</h4> */}
          <p className="text-red-500">{message}</p>
          
          {/* Close icon in the top-right corner */}
          <span
            onClick={onClose}
            className="absolute top-2 right-2 cursor-pointer text-2xl text-gray-600 hover:text-gray-800"
          >
            &times; {/* This is the "X" icon for close */}
          </span>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-bgColor-400 h-screen py-16">
      <h4 className="font-bold text-3xl text-black mb-6 items-center text-center">{randomText}</h4>

      <PlaceholdersAndVanishInput
        placeholders={placeholders}
        onChange={(e) => setMessage(e.target.value)}
        onSubmit={getSymptom}
      />

      {loading && (
        <div className="bg-bgColor-300 m-12 mt-20 rounded-md p-4">
          <h5 className="font-bold text-2xl text-black mb-6 text-center mt-6">
            Based on your symptoms, you may have one of these conditions.
          </h5>
          <div className="bg-bgColor-200 p-8 border-black rounded-sm border-2 ml-16 mr-16 text-center">
            {diseases.map((item, index) => (
              <button
                key={index}
                className="bg-white p-4 text-xl rounded-xl mr-8 hover:bg-slate-400"
                onClick={() => handleNextPage(item)}
              >
                {item}
              </button>
            ))}
          </div>
          <h5 className="font-bold text-2xl text-black mb-6 text-center mt-6">
            To get a more accurate diagnosis, we recommend clicking on an illness.
          </h5>
        </div>
      )}

      {!loading && (
        <div className="w-full hidden sm:block">
          <Spline
            className="spline 
            md:spline-024 
            sm:spline-100 
            xs:spline-200 
            xxs:spline-75
            mr-10 absolute top-10 left-15"
            scene="https://prod.spline.design/ZCJFcd6hmEDt89SB/scene.splinecode"
          />
          <Spline
            className="spline 
            md:spline-1024 
            sm:spline-100 
            xs:spline-200 
            xxs:spline-375
            mr-10 absolute top-10 right-0"
            scene="https://prod.spline.design/ZCJFcd6hmEDt89SB/scene.splinecode"
          />
        </div>
      )}

      {/* Show the error modal if error state is set */}
      {error && <ErrorModal message={error} onClose={() => setError('')} />}
    </div>
  );
};

export default FindSymptoms;
