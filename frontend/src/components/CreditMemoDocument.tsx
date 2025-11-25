interface CreditMemoDocumentProps {
  memo: string;
  businessName: string;
  loanAmount: number;
  recommendation: string;
  underwritingScore: number;
  date?: string;
}

export default function CreditMemoDocument({
  memo,
  businessName,
  loanAmount,
  recommendation,
  underwritingScore,
  date = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}: CreditMemoDocumentProps) {
  const getRecommendationColor = (rec: string) => {
    switch (rec) {
      case 'APPROVE': return 'text-green-700 bg-green-50 border-green-200';
      case 'APPROVE_WITH_CONDITIONS': return 'text-yellow-700 bg-yellow-50 border-yellow-200';
      case 'DECLINE': return 'text-red-700 bg-red-50 border-red-200';
      default: return 'text-gray-700 bg-gray-50 border-gray-200';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-700';
    if (score >= 60) return 'text-yellow-700';
    return 'text-red-700';
  };

  return (
    <div className="bg-white border-2 border-gray-300 rounded-lg shadow-2xl overflow-hidden animate-scale-in">
      {/* Document Header - Professional Letterhead Style */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white px-8 py-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">CREDIT MEMO</h1>
            <p className="text-blue-100 mt-1 text-sm">Multi-Agent AI Financial Analysis</p>
          </div>
          <div className="text-right">
            <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
              <p className="text-xs text-blue-100">Document Date</p>
              <p className="text-sm font-semibold">{date}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Applicant Information Bar */}
      <div className="bg-gradient-to-r from-gray-50 to-white border-b-2 border-gray-200 px-8 py-4">
        <div className="grid grid-cols-3 gap-6">
          <div>
            <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Applicant</p>
            <p className="text-lg font-bold text-gray-900 mt-1">{businessName}</p>
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Loan Amount</p>
            <p className="text-lg font-bold text-gray-900 mt-1">${loanAmount.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Analysis Score</p>
            <p className={`text-2xl font-bold mt-1 ${getScoreColor(underwritingScore)}`}>
              {underwritingScore}/100
            </p>
          </div>
        </div>
      </div>

      {/* Executive Summary Badge */}
      <div className="px-8 py-6 bg-gray-50">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-600 mb-2">CREDIT DECISION</p>
            <div className={`inline-flex items-center px-6 py-3 rounded-full border-2 font-bold text-lg ${getRecommendationColor(recommendation)}`}>
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                {recommendation === 'APPROVE' ? (
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                ) : recommendation === 'DECLINE' ? (
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                ) : (
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                )}
              </svg>
              {recommendation.replace(/_/g, ' ')}
            </div>
          </div>
          <div className="text-right">
            <p className="text-xs text-gray-500">Analyzed by</p>
            <p className="text-sm font-semibold text-gray-700">AI Multi-Agent System</p>
            <p className="text-xs text-gray-500 mt-1">3 Specialized Agents</p>
          </div>
        </div>
      </div>

      {/* Main Content - Credit Memo */}
      <div className="px-8 py-6">
        <div className="prose prose-sm max-w-none">
          <div className="whitespace-pre-wrap text-gray-800 leading-relaxed custom-scrollbar max-h-96 overflow-y-auto bg-white p-6 rounded-lg border border-gray-200">
            {memo.split('\n\n').map((paragraph, idx) => {
              // Check if paragraph is a heading (starts with **)
              if (paragraph.trim().startsWith('**') && paragraph.trim().endsWith('**')) {
                const headingText = paragraph.replace(/\*\*/g, '').trim();
                return (
                  <h3 key={idx} className="text-xl font-bold text-gray-900 mt-6 mb-3 first:mt-0 border-b-2 border-blue-600 pb-2">
                    {headingText}
                  </h3>
                );
              }

              // Regular paragraph
              return (
                <p key={idx} className="mb-4 text-gray-700 text-justify leading-relaxed">
                  {paragraph.split('**').map((part, i) =>
                    i % 2 === 0 ? part : <strong key={i} className="font-semibold text-gray-900">{part}</strong>
                  )}
                </p>
              );
            })}
          </div>
        </div>
      </div>

      {/* Document Footer */}
      <div className="bg-gradient-to-r from-gray-100 to-gray-50 border-t-2 border-gray-300 px-8 py-4">
        <div className="flex justify-between items-center text-xs text-gray-600">
          <div className="flex items-center space-x-4">
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              AI-Verified Analysis
            </span>
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
              </svg>
              Confidential Document
            </span>
          </div>
          <p className="text-gray-500">
            Generated by Multi-Agent AI Financial Analyzer • Powered by OpenAI GPT-4o-mini
          </p>
        </div>
      </div>
    </div>
  );
}
