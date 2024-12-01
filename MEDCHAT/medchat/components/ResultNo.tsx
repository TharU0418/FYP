import React, { useEffect, useState } from 'react';

const ResultNo = () => {
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

    return (
        <div className='bg-blue-950 h-screen py-16  text-center items-center justify-center'>
            <div className='bg-white p-8 border-black rounded-sm border-2 ml-16 mr-16 text-center'>
            
            <h3 className='font-bold mb-6'>Seems like you doesn't diagonse from </h3>
            
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
    );
};

export default ResultNo;
