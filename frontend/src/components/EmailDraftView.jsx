const EmailDraftView = ({ text }) => {
  const copyToClipboard = () => {
    navigator.clipboard.writeText(text);
    alert("Copied to clipboard!");
  };

  return (
    <section className="bg-gray-900 text-white p-6 rounded-lg">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Follow-up Email Draft</h2>
        <button onClick={copyToClipboard} className="text-sm bg-blue-600 px-3 py-1 rounded hover:bg-blue-500">
          Copy Email
        </button>
      </div>
      <pre className="whitespace-pre-wrap font-sans text-gray-300 bg-gray-800 p-4 rounded">
        {text}
      </pre>
    </section>
  );
};
export default EmailDraftView;