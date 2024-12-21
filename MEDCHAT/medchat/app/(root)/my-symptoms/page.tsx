'use client';
import { useSearchParams, useRouter } from 'next/navigation';
import React, { useEffect, useState } from 'react';
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";

const MySymptoms = () => {
  const searchParams = useSearchParams();
  const disease = searchParams.get('disease');
  const [symptoms, setSymptoms] = useState<string[]>([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]); // Track selected symptoms
  const [result, setResult] = useState<string>();

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

const router = useRouter();

  const handleSubmit = async() => {
    console.log('Selected Symptoms:', selectedSymptoms); // You can handle further logic here
    const cleanedSymptoms = selectedSymptoms.map(symptom => symptom.replace(/_/g, ' ').trim());
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
      setResult(data.predicted_illness); // Assuming data.result contains the result
      console.log('result', data.predicted_illness)
      handleResultPage(data.predicted_illness);
};

const handleResultPage = (result: string) => {
    router.push(`/results?result=${result}`);
  }

  return (
    <div className='bg-bgColor-400 h-screen py-16'>
        <div className='bg-transparent bg-white p-6 m-4 rounded-lg'>
          <h1 className='text-3xl font-bold text-center mt-8 mb-5'>Let's ckeck you have: {disease}</h1>
          <h4 className='text-xl font-bold text-center mt-8 mb-6'>Click all the symptoms that you experience right now</h4>

          <ToggleGroup type="multiple" className="mt-6 grid grid-cols-6 gap-4 items-center">
            {symptoms.map((symptom) => (
              <ToggleGroupItem key={symptom} value={symptom} className=' mb-8'>
                  <button
                  className={`bg-blue-500 text-white p-6 text-xl border-r-2 rounded-xl hover:text-white' ${selectedSymptoms.includes(symptom) ? 'bg-blue-950 text-white' : ''}`}
                  onClick={() => handleToggle(symptom)}
                  >
                  {symptom}
                  </button>
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
