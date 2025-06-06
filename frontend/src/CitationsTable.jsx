import React from 'react';

const CitationsTable = ({ citations }) => {
  if (!citations || citations.length === 0) return null;

  // Get all unique keys from all citation objects to create dynamic columns
  const getAllKeys = (items) => {
    const keysSet = new Set();
    items.forEach(item => {
      Object.keys(item).forEach(key => {
        if (key !== 'id') { // Exclude 'id' column
          keysSet.add(key);
        }
      });
    });
    return Array.from(keysSet);
  };

  // Format column headers (convert snake_case to Title Case)
  const formatHeader = (key) => {
    return key
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  // Format cell values
  const formatCellValue = (value, key) => {
    if (value === null || value === undefined) return 'N/A';

    // Format price with $ symbol
    if (key === 'price' && typeof value === 'number') {
      return `$${value}`;
    }

    // Convert arrays to comma-separated strings
    if (Array.isArray(value)) {
      return value.join(', ');
    }

    return String(value);
  };

  const columns = getAllKeys(citations);

  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Recommended Items</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200 rounded-lg">
          <thead className="bg-gray-50">
            <tr>
              {columns.map((column) => (
                <th
                  key={column}
                  className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b whitespace-nowrap"
                >
                  {formatHeader(column)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {citations.map((item, index) => (
              <tr key={item.id || index} className="hover:bg-gray-50">
                {columns.map((column) => (
                  <td
                    key={column}
                    className={`px-4 py-3 text-sm ${
                      column === 'price' ? 'font-semibold text-gray-900' :
                      'text-gray-700'
                    } ${column === 'category' ? 'capitalize' : ''}`}
                  >
                    {formatCellValue(item[column], column)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CitationsTable;
