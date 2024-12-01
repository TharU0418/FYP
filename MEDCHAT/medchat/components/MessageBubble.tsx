import React from 'react';

interface MessageBubbleProps {
  text: string;
  sender: 'bot' | 'user';
  options?: string[];
  onOptionClick: (option: string) => void;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ text, sender, options, onOptionClick }) => {
  return (
    <div className={`rounded-lg p-3 max-w-[70%] my-2 mb-8 ${sender === 'bot' ? 'bg-gray-200 text-black self-start' : 'bg-blue-500 text-white self-end'}`}>
      <div dangerouslySetInnerHTML={{ __html: text }} /> {/* Safely render HTML */}
      {options && (
        <div className="mt-2">
          {options.map((option, index) => (
            <button 
              key={index} 
              className="inline-block bg-green-100 hover:bg-green-200 text-black py-2 px-4 rounded-md mr-2 mt-2" 
              onClick={() => onOptionClick(option)} 
              dangerouslySetInnerHTML={{ __html: option }} 
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default MessageBubble;
