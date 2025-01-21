'use client';
import { useSearchParams, useRouter } from 'next/navigation';
import React, { useEffect, useState } from 'react';
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import intenseData from './intense.json';

const MySymptoms = () => {
  const searchParams = useSearchParams();
  const disease = searchParams.get('disease');
  const [symptoms, setSymptoms] = useState<string[]>([]);
  //const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]); // Track selected symptoms
  const [selectedSymptoms, setSelectedSymptoms] = useState<string>(''); // Track selected symptoms as a single string

  const [result, setResult] = useState<string>();
  const symptomsData = intenseData.symptoms;

  const disease1 = disease

  console.log('symptomsData', symptomsData)
  console.log('diseaes disease', disease)


  const GetSymptoms = async () => {
    const res = await fetch('http://127.0.0.1:5000/get_illess_name', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        diseases_input: disease,
      }),
    });
    const data = await res.json();
    setSymptoms(data.symptoms);
  };

  useEffect(() => {
    GetSymptoms();
  }, []); // Empty dependency array ensures this runs only once

  const handleToggle = (symptom: string) => {
    setSelectedSymptoms((prevSelected) =>
      prevSelected.includes(symptom)
        ? prevSelected.filter((s) => s !== symptom) // Remove if already selected
        : [...prevSelected, symptom] // Add if not selected
    );
  };



// const handleToggle = (symptom: string) => {
//   setSelectedSymptoms((prevSelected) => {
//     const symptomsArray = prevSelected ? prevSelected.split(', ') : []; // Convert string to array if there are any selected symptoms
//     const isSymptomSelected = symptomsArray.includes(symptom);

//     if (isSymptomSelected) {
//       // Remove the symptom from the array if it's already selected
//       const updatedSymptoms = symptomsArray.filter(s => s !== symptom);
//       return updatedSymptoms.join(', '); // Join them back as a single string
//     } else {
//       // Add the symptom to the array if it's not selected
//       const updatedSymptoms = [...symptomsArray, symptom];
//       return updatedSymptoms.join(', '); // Join them back as a single string
//     }
//   });
// };


const router = useRouter();

  const handleSubmit = async() => {
    console.log('Selected Symptoms:', selectedSymptoms); // You can handle further logic here
    //const cleanedSymptoms = selectedSymptoms.map(symptom => symptom.replace(/_/g, ' ').trim());
    const cleanedSymptoms =  selectedSymptoms.join(", "); // Convert array to comma-separated string

   //// const cleanedSymptoms = selectedSymptoms.map(symptom => {
      // Now you can directly use .map() because selectedSymptoms is an array
   /// /  console.log(symptom); // Replace with your actual logic
   //// });
    console.log('Selected Symptoms:', cleanedSymptoms); // You can handle further logic here

    const res = await fetch('http://127.0.0.1:5000/predictthediseases', {
        method : 'POST',
        headers: {
          'Content-Type' : 'application/json',
        },
        body: JSON.stringify({
          symptoms: cleanedSymptoms
        })
      });
      const data = await res.json();
      console.log('data', data)
      setResult(data.predicted_disease); // Assuming data.result contains the result
      console.log('result', data.predicted_disease)
      handleResultPage(data.predicted_disease, disease1);
};

const handleResultPage = (result: string) => {
  router.push(`/results?result=${result}&disease=${disease1}`);
};

  const getSymptomDescription = (symptom: string) => {
    const symptomData = symptomsData.find((item) => item.name === symptom);
    return symptomData ? symptomData.description : "Description not available.";
  };

  
  return (
    <div className='bg-bgColor-700 h-screen py-16'>
        <div className='bg-white p-6 m-4 rounded-lg'>
          <h1 className='text-3xl font-bold text-center mt-8 mb-5'>Let's ckeck you have: {disease}</h1>
          <h4 className='text-xl font-bold text-center mt-8 mb-16'>Click all the symptoms that you experience right now</h4>

          <ToggleGroup type="multiple" className="mt-6 grid grid-cols-5 gap-4 items-center">
  {symptoms.map((symptom) => (
    <ToggleGroupItem key={symptom} value={symptom} className=' mb-8'>
      <div className="relative">
        <button
          className={`bg-blue-500 text-white p-4 text-xl border-r-2 rounded-xl hover:text-white ${selectedSymptoms.includes(symptom) ? 'bg-blue-950 text-white' : ''}`}
          onClick={() => handleToggle(symptom)}
        >
          {symptom.replace(/_/g, ' ').replace(/^\w/, (c) => c.toUpperCase())}

        </button>
        <div className="w-60 absolute left-1/2 transform -translate-x-1/2 bottom-full mb-2 hidden group-hover:block bg-black text-white text-x p-2 rounded-md">
          {getSymptomDescription(symptom)}
        </div>

      </div>
    </ToggleGroupItem>
  ))}
</ToggleGroup>


        <div className="flex justify-center w-full mt-8">
          <button
            onClick={handleSubmit}
            className="text-xl mt-4 bg-green-500 hover:bg-green-600 text-white font-semibold py-4 px-10 rounded">
              SUBMIT
          </button>
        </div>
      </div>
    </div>
  );
};

export default MySymptoms;
