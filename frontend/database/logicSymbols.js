import { FiCode, FiArrowRight, FiRepeat, FiX, FiCornerDownLeft } from 'react-icons/fi';

const logicSymbols = [
  { 
    id: 1, 
    name: 'AND', 
    symbol: <FiCode className="logic-icon" />,
    description: 'Logical AND' 
  },
  { 
    id: 2, 
    name: 'OR', 
    symbol: <FiCornerDownLeft className="logic-icon" />,
    description: 'Logical OR' 
  },
  { 
    id: 3, 
    name: 'NOT', 
    symbol: <FiX className="logic-icon" />,
    description: 'Logical NOT' 
  },
  { 
    id: 4, 
    name: 'IMPLY', 
    symbol: <FiArrowRight className="logic-icon" />,
    description: 'Logical If...then' 
  },
  { 
    id: 5, 
    name: 'EQUIV', 
    symbol: <FiRepeat className="logic-icon" />,
    description: 'Logical If and only if' 
  },
];

export default logicSymbols;