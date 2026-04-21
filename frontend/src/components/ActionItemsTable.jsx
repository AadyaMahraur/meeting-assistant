const ActionItemsTable = ({ items }) => (
  <div className="bg-white shadow rounded-lg p-4">
    <h2 className="text-xl font-bold mb-4">Action Items</h2>
    <table className="w-full text-left border-collapse">
      <thead>
        <tr className="border-b text-sm text-gray-600">
          <th className="py-2">Task</th>
          <th>Owner</th>
          <th>Priority</th>
        </tr>
      </thead>
      <tbody>
        {items.map((item, i) => (
          <tr key={i} className="border-b last:border-0 hover:bg-gray-50">
            <td className="py-3 pr-2">{item.description}</td>
            <td className="text-sm font-medium">{item.owner}</td>
            <td>
              <span className={`px-2 py-1 rounded text-xs uppercase font-bold ${
                item.priority === 'high' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'
              }`}>
                {item.priority}
              </span>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);
export default ActionItemsTable;