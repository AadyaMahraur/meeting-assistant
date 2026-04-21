import React from 'react';

const DecisionsList = ({ items }) => {
  return (
    <div className="bg-white shadow rounded-lg p-5 border-t-4 border-green-500">
      <h2 className="text-xl font-bold mb-4 flex items-center">
        <span className="mr-2">✅</span> Decisions Made
      </h2>
      {items.length === 0 ? (
        <p className="text-gray-500 italic">No specific decisions were recorded.</p>
      ) : (
        <ul className="space-y-4">
          {items.map((decision, index) => (
            <li key={index} className="flex flex-col border-b border-gray-100 pb-3 last:border-0">
              <span className="text-gray-800 font-medium">{decision.description}</span>
              <span className="text-xs text-gray-500 mt-1 uppercase tracking-wide">
                Decided by: {decision.decided_by}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DecisionsList;