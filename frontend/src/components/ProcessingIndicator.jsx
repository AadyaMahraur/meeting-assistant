import React from 'react';

const ProcessingIndicator = () => {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4">
      <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      <p className="text-gray-600 font-medium">Loading</p>
    </div>
  );
};

export default ProcessingIndicator;