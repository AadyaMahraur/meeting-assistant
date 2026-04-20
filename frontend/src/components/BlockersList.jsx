import React from 'react';

const BlockersList = ({ items }) => {
  // Helper to color-code the types
  const getTypeStyles = (type) => {
    switch (type.toLowerCase()) {
      case 'blocker': return 'bg-red-100 text-red-700 border-red-200';
      case 'risk': return 'bg-orange-100 text-orange-700 border-orange-200';
      case 'open_question': return 'bg-blue-100 text-blue-700 border-blue-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-5">
      <h2 className="text-xl font-bold mb-4 flex items-center">
        <span className="mr-2">🚧</span> Blockers & Risks
      </h2>
      {items.length === 0 ? (
        <p className="text-gray-500 italic">No blockers or risks were identified.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {items.map((blocker, index) => (
            <div key={index} className="p-4 border rounded-lg flex flex-col justify-between">
              <div>
                <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${getTypeStyles(blocker.type)}`}>
                  {blocker.type.replace('_', ' ')}
                </span>
                <p className="mt-2 text-gray-800">{blocker.description}</p>
              </div>
              <div className="mt-3 pt-3 border-t border-gray-50 text-xs text-gray-500 italic">
                Raised by: {blocker.raised_by}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BlockersList;