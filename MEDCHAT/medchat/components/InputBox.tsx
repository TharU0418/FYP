'use client';
import React, { useState } from 'react';
import { ButtonsCard } from './ui/tailwindcss-buttons';

interface InputBoxProps {
  onSendMessage: (message: string) => void;
}

const InputBox: React.FC<InputBoxProps> = ({ onSendMessage }) => {
  const [message, setMessage] = useState<string>('');

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(message);
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <div className="flex">
      <form className="flex flex-row p-6 bg-white border-t-2 border-black mt-auto w-full" onSubmit={handleSubmit}>
        <div className='w-8/12'>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-4 border-1 border-white rounded-s w-full bg-slate-500 text-white"
          />
        </div>
        <div className='w-4/12'>
          {buttons.map((button, idx) => (
            <ButtonsCard key={idx} onClick={() => button}>
              {button.component}
            </ButtonsCard>
          ))}
        </div>
      </form>
    </div>
  );
};

export default InputBox;

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
      <button className="px-12 py-2 rounded-md bg-blue-800 text-white font-bold transition duration-200 hover:bg-blue-300 hover:text-black border-2 border-transparent hover:border-teal-500">
        <img
        src='/icons/send.png'
        width={40}
        height={40}
        />
      </button>
    ),
  },
];
