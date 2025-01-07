import React, { useEffect, useState } from 'react';
import { BackgroundGradient } from './ui/background-gradient';

interface ResultProps {
    pass : string
}

const ResultNo = ({pass}) => {
    const [other, setOther] = useState<Record<string, boolean> | null>(null);

    useEffect(() => {
        // Only runs on the client side
        const savedDetails = JSON.parse(localStorage.getItem('details') || '{}');
        setOther(savedDetails);
    }, []);

    // Define the handleNextPage function
    const handleNextPage = (item: string) => {
        console.log('Clicked:', item);
        // Add your logic to handle the next page or action
    };

    console.log('pass', pass)

    return (
        <div className='bg-blue-950 h-screen py-16  text-center items-center justify-center'>
            {/* <div className='bg-white p-8 border-black rounded-sm border-2 ml-16 mr-16 text-center'> */}
            <div className='m-6'>
        <BackgroundGradient className="rounded-[22px] p-4 sm:p-10 bg-white dark:bg-zinc-900 m-2">
            
            <h3 className='font-bold mb-2'>Seems like you doesn't diagonse from </h3>
            
            <p className='text-blue-500 font-bold text-2xl mb-6'>{pass}</p>

            <h5 className='font-bold text-2xl text-blue-200 mb-6 text-center mt-10'>
        Explore other diagnoses
      </h5>

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
                        </BackgroundGradient>
</div>
            </div>
    );
};

export default ResultNo;
