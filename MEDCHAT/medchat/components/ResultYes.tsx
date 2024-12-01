import { useRouter } from 'next/navigation';
import React, { useEffect, useState } from 'react'

interface ResultProps {
    diseaes: string,
    disc: string[]
    prevention:string[]
}

const ResultYes: React.FC<ResultProps> = ({diseaes, disc, prevention}) => {

    console.log('prevention', prevention)

    const [other, setOther] = useState<Record<string, boolean> | null>(null);

    useEffect(() => {
        // Only runs on the client side
        const savedDetails = JSON.parse(localStorage.getItem('details') || '{}');
        setOther(savedDetails);
    }, []);

    // Define the handleNextPage function
    const handleNextPage = (item: string) => {
        router.push(`/my-symptoms?disease=${encodeURIComponent(item)}`)
    };
    const router = useRouter();

    const handleNextDiseasePage = (item: string) => {
    }


  return (
    <div className='bg-blue-950 h-screen py-16  text-center items-center justify-center'>

        <div className='bg-white bg-transparent ml-10 py-5 rounded-sm mb-6' style={{width:'92%'}}>
            <h4 className='text-black text-xl font-bold mt-4'>Based on your answes your most liekly to digonse by</h4>
            <p className='text-blue-500 font-bold text-2xl mt-6'>{diseaes}</p>

            <p className='text-sm mt-6 w-3/4 '>{disc}</p>

            <h3 className='text-left font-bold mt-8 ml-4'>Prevention & Treatment</h3>
            <p className='text-left ml-6'>{prevention.join(', ')}</p>


        </div>


        <h5 className='font-bold text-2xl text-white mb-6 text-center mt-10'>
        If you want to check other illnesses click 
      </h5>

            <div className='bg-blue-500 p-8 border-black rounded-sm border-2 ml-16 mr-16 text-center'>



                {other && Object.entries(other).map(([key, value]) => (
                    <button
                        key={key}
                        className='text-white p-4 text-xl rounded-xl mr-8 hover:bg-slate-400'
                        onClick={() => handleNextPage(key)}
                        disabled={!value} // Disable the button if value is false
                        style={{ backgroundColor: value ? 'green' : 'red' }}
                        
                    >
                        {key}
                        </button>
                ))}
            </div>
    </div>
  )
}

export default ResultYes