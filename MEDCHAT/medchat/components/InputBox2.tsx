'use client';
import React, { useEffect, useState } from 'react';
import { ButtonsCard } from './ui/tailwindcss-buttons';

interface InputBoxProps {
  onSendMessage: (message: string) => void;
}

const InputBox2: React.FC<InputBoxProps> = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');

  const getSentence = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();  // Prevents the form from refreshing the page
    console.log(message); // Prints the input value to the console

    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }

  }

                                                                                                          

  return (
    <div className="flex">
      <form className="flex flex-row p-6 mt-auto w-full">
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
        onClick={getSentence}
      >
        Submit
        </button>
        </div>
      </form>
    </div>
  );
};

export default InputBox2;

interface Button {
  name: string;
  description: string;
  component: React.ReactNode;
}

export const buttons: Button[] = [
  {
    name: 'Invert',
    description: 'Simple button that inverts on hover',
    component: (
      <button className="px-12 py-3 rounded-md bg-blue-900 text-white font-bold transition duration-200 hover:bg-blue-800 hover:text-black ml-4">
        <img
        src='/icons/send.png'
        width={40}
        height={40}
        />
      </button>
    ),
  },
];
