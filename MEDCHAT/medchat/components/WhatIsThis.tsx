'use client';

import { TextGenerateEffect } from "./ui/text-generate-effect";


const words = `Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam convallis eleifend ligula non ultrices. Duis viverra ultrices interdum. 
Nam nec cursus turpis. Nunc ut rutrum sapien. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam vitae ligula convallis, 
tincidunt dui eu, luctus mi. Proin sit amet nulla consectetur, volutpat justo et, venenatis libero. Nulla at mi aliquet, molestie nunc nec, pellentesque nunc. 
Pellentesque tristique mauris consectetur, sollicitudin lectus vitae, sollicitudin massa. Nullam viverra dui eget sagittis iaculis. Sed varius sagittis dui at tempor.
 Mauris ut sodales nisl.`;

export function WhatIsTHis() {
  return (
      <div className="flex flex-col items-center justify-center w-4xl p-6 ml-8 mr-8 bg-blue-800 rounded-2xl">
        <h2 className="text-4xl font-bold text-white mb-4">WHAT IS MEDCHAT</h2>
          <TextGenerateEffect words={words}/>
      </div>
  );
}