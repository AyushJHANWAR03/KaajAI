import { useState } from 'react';
import axios from 'axios';
import { AnalyzeRequest, AnalysisResponse } from './types';
import CreditMemoDocument from './components/CreditMemoDocument';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const steps = [
  { id: 1, name: 'Business Info', description: 'Company details' },
  { id: 2, name: 'Loan Details', description: 'Loan terms' },
  { id: 3, name: 'Bank Data', description: 'Bank statements' },
  { id: 4, name: 'Tax Data', description: 'Tax returns (optional)' },
  { id: 5, name: 'Review', description: 'Confirm details' },
  { id: 6, name: 'Results', description: 'Analysis complete' },
];

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [interestRateDisplay, setInterestRateDisplay] = useState('8.0');

  // Form state with default demo values (ABC Construction LLC - APPROVE scenario)
  const [formData, setFormData] = useState({
    business_name: 'ABC Construction LLC',
    industry: 'Construction',
    business_age_years: 5,
    loan_amount: 50000,
    annual_interest_rate: 0.08,
    term_months: 60,
    existing_debt: 80000,
    monthly_deposits: '42000, 38000, 51000, 45000, 43000, 47000, 46000, 44000, 49000, 45000, 44000, 46000',
    monthly_withdrawals: '35000, 32000, 38000, 36000, 34000, 37000, 36000, 35000, 38000, 36000, 35000, 37000',
    nsf_fees: 1,
    average_balance: 15000,
    months_covered: 12,
    include_tax_data: true,
    gross_revenue: 540000,
    total_expenses: 420000,
    net_income: 120000,
    tax_year: 2024,
  });

  const handleNext = () => {
    if (currentStep === 4 && !formData.include_tax_data) {
      setCurrentStep(5); // Skip to review if tax data not included
    } else if (currentStep < 6) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep === 5 && !formData.include_tax_data) {
      setCurrentStep(3); // Skip back over tax data step
    } else if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const requestData: AnalyzeRequest = {
        business_name: formData.business_name,
        industry: formData.industry,
        loan_amount: formData.loan_amount,
        business_age_years: formData.business_age_years,
        annual_interest_rate: formData.annual_interest_rate,
        term_months: formData.term_months,
        existing_debt: formData.existing_debt,
        bank_data: {
          monthly_deposits: formData.monthly_deposits.split(',').map(n => parseFloat(n.trim())),
          monthly_withdrawals: formData.monthly_withdrawals.split(',').map(n => parseFloat(n.trim())),
          nsf_fees: formData.nsf_fees,
          average_balance: formData.average_balance,
          months_covered: formData.months_covered,
        },
      };

      if (formData.include_tax_data) {
        requestData.tax_data = {
          gross_revenue: formData.gross_revenue,
          total_expenses: formData.total_expenses,
          net_income: formData.net_income,
          tax_year: formData.tax_year,
        };
      }

      const response = await axios.post<AnalysisResponse>(`${API_URL}/api/analyze`, requestData);
      setResult(response.data);
      setCurrentStep(6); // Move to results step
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleStartOver = () => {
    setCurrentStep(1);
    setResult(null);
    setError(null);
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'LOW': return 'text-green-600 bg-green-100';
      case 'MODERATE': return 'text-yellow-600 bg-yellow-100';
      case 'HIGH': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getRecommendationColor = (rec: string) => {
    switch (rec) {
      case 'APPROVE': return 'text-green-600 bg-green-100';
      case 'APPROVE_WITH_CONDITIONS': return 'text-yellow-600 bg-yellow-100';
      case 'DECLINE': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-sm border-b border-gray-200/50 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Multi-Agent Kaaj AI Financial Analyzer
              </h1>
              <p className="mt-1 text-sm text-gray-600">Automated Loan Underwriting System</p>
            </div>
            <div className="hidden md:flex items-center space-x-2 text-sm text-gray-500">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
              </svg>
              <span></span>
            </div>
          </div>
        </div>
      </header>

      {/* Modern Progress Indicator */}
      <div className="bg-white/60 backdrop-blur-sm border-b border-gray-200/50">
        <div className="max-w-6xl mx-auto px-4 py-8">
          <div className="relative">
            {/* Progress Line Background */}
            <div className="absolute top-6 left-0 w-full h-1 bg-gray-200 rounded-full" style={{ left: '2rem', width: 'calc(100% - 4rem)' }} />

            {/* Active Progress Line */}
            <div
              className="absolute top-6 left-0 h-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full transition-all duration-500 ease-out"
              style={{
                left: '2rem',
                width: `calc((100% - 4rem) * ${(currentStep - 1) / (steps.length - 1)})`
              }}
            />

            {/* Steps */}
            <div className="relative flex justify-between">
              {steps.map((step) => (
                <div key={step.id} className="flex flex-col items-center" style={{ width: '140px' }}>
                  {/* Circle */}
                  <div className="relative z-10 mb-3">
                    <div
                      className={`h-12 w-12 rounded-full flex items-center justify-center transition-all duration-300 ${
                        step.id < currentStep
                          ? 'bg-gradient-to-br from-blue-600 to-purple-600 shadow-lg scale-100'
                          : step.id === currentStep
                          ? 'bg-gradient-to-br from-blue-600 to-purple-600 shadow-xl scale-110 ring-4 ring-blue-200'
                          : 'bg-white border-2 border-gray-300 scale-90'
                      }`}
                    >
                      {step.id < currentStep ? (
                        <svg className="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      ) : (
                        <span className={`text-base font-bold ${step.id === currentStep ? 'text-white' : 'text-gray-400'}`}>
                          {step.id}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Label */}
                  <div className="text-center">
                    <p className={`text-sm font-semibold mb-1 transition-colors ${
                      step.id === currentStep
                        ? 'text-blue-700'
                        : step.id < currentStep
                        ? 'text-blue-600'
                        : 'text-gray-400'
                    }`}>
                      {step.name}
                    </p>
                    <p className={`text-xs ${
                      step.id <= currentStep ? 'text-gray-600' : 'text-gray-400'
                    }`}>
                      {step.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-2xl border border-gray-200/50 p-8 animate-fade-in">
          {/* Step 1: Business Information */}
          {currentStep === 1 && (
            <div className="space-y-6 animate-slide-in">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Business Information</h2>
                <p className="mt-2 text-sm text-gray-600">Tell us about your business</p>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Business Name</label>
                  <input
                    type="text"
                    value={formData.business_name}
                    onChange={(e) => setFormData({ ...formData, business_name: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter your business name"
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Industry</label>
                    <select
                      value={formData.industry}
                      onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="Construction">Construction</option>
                      <option value="Manufacturing">Manufacturing</option>
                      <option value="Retail">Retail</option>
                      <option value="Restaurant">Restaurant</option>
                      <option value="Healthcare">Healthcare</option>
                      <option value="Professional Services">Professional Services</option>
                      <option value="Technology">Technology</option>
                      <option value="Transportation">Transportation</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Business Age (years)</label>
                    <input
                      type="number"
                      value={formData.business_age_years === 0 ? '' : formData.business_age_years}
                      onChange={(e) => {
                        const value = e.target.value === '' ? 0 : parseInt(e.target.value);
                        setFormData({ ...formData, business_age_years: value });
                      }}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="e.g., 5"
                      min="0"
                      required
                    />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Loan Details */}
          {currentStep === 2 && (
            <div className="space-y-6 animate-slide-in">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Loan Details</h2>
                <p className="mt-2 text-sm text-gray-600">Specify the loan terms you're requesting</p>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Loan Amount ($)</label>
                    <input
                      type="number"
                      value={formData.loan_amount === 0 ? '' : formData.loan_amount}
                      onChange={(e) => {
                        const value = e.target.value === '' ? 0 : parseFloat(e.target.value);
                        setFormData({ ...formData, loan_amount: value });
                      }}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="e.g., 50000"
                      min="0"
                      step="1000"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Term (months)</label>
                    <input
                      type="number"
                      value={formData.term_months === 0 ? '' : formData.term_months}
                      onChange={(e) => {
                        const value = e.target.value === '' ? 0 : parseInt(e.target.value);
                        setFormData({ ...formData, term_months: value });
                      }}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="e.g., 60"
                      min="1"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Annual Interest Rate</label>
                    <div className="relative">
                      <input
                        type="text"
                        inputMode="decimal"
                        value={interestRateDisplay}
                        onChange={(e) => {
                          const inputValue = e.target.value;
                          // Allow empty, digits, and one decimal point
                          if (inputValue === '' || /^\d*\.?\d*$/.test(inputValue)) {
                            setInterestRateDisplay(inputValue);
                            // Update form data with parsed value
                            const numValue = parseFloat(inputValue) || 0;
                            const clampedValue = Math.min(Math.max(numValue, 0), 30);
                            setFormData({ ...formData, annual_interest_rate: clampedValue / 100 });
                          }
                        }}
                        onBlur={(e) => {
                          // Format to 1 decimal place on blur
                          const value = parseFloat(e.target.value) || 0;
                          const clampedValue = Math.min(Math.max(value, 0), 30);
                          setInterestRateDisplay(clampedValue.toFixed(1));
                          setFormData({ ...formData, annual_interest_rate: clampedValue / 100 });
                        }}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="8.0"
                        required
                      />
                      <span className="absolute right-4 top-3 text-gray-500">%</span>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Existing Debt ($)</label>
                    <input
                      type="number"
                      value={formData.existing_debt === 0 ? '' : formData.existing_debt}
                      onChange={(e) => {
                        const value = e.target.value === '' ? 0 : parseFloat(e.target.value);
                        setFormData({ ...formData, existing_debt: value });
                      }}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="e.g., 80000"
                      min="0"
                      step="1000"
                      required
                    />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Step 3: Bank Statement Data */}
          {currentStep === 3 && (
            <div className="space-y-6 animate-slide-in">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Bank Statement Data</h2>
                <p className="mt-2 text-sm text-gray-600">Provide 12 months of bank statement data</p>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Monthly Deposits (12 months, comma-separated)
                  </label>
                  <textarea
                    value={formData.monthly_deposits}
                    onChange={(e) => setFormData({ ...formData, monthly_deposits: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows={3}
                    placeholder="42000, 38000, 51000, ..."
                    required
                  />
                  <p className="mt-1 text-xs text-gray-500">Enter 12 monthly deposit amounts separated by commas</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Monthly Withdrawals (12 months, comma-separated)
                  </label>
                  <textarea
                    value={formData.monthly_withdrawals}
                    onChange={(e) => setFormData({ ...formData, monthly_withdrawals: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows={3}
                    placeholder="35000, 32000, 38000, ..."
                    required
                  />
                  <p className="mt-1 text-xs text-gray-500">Enter 12 monthly withdrawal amounts separated by commas</p>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">NSF Fees</label>
                    <input
                      type="number"
                      value={formData.nsf_fees === 0 ? '' : formData.nsf_fees}
                      onChange={(e) => {
                        const value = e.target.value === '' ? 0 : parseInt(e.target.value);
                        setFormData({ ...formData, nsf_fees: value });
                      }}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="e.g., 0"
                      min="0"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Avg Balance ($)</label>
                    <input
                      type="number"
                      value={formData.average_balance === 0 ? '' : formData.average_balance}
                      onChange={(e) => {
                        const value = e.target.value === '' ? 0 : parseFloat(e.target.value);
                        setFormData({ ...formData, average_balance: value });
                      }}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="e.g., 15000"
                      min="0"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Months Covered</label>
                    <input
                      type="number"
                      value={formData.months_covered}
                      onChange={(e) => setFormData({ ...formData, months_covered: parseInt(e.target.value) || 12 })}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="12"
                      min="1"
                      max="12"
                    />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Step 4: Tax Return Data */}
          {currentStep === 4 && (
            <div className="space-y-6 animate-slide-in">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Tax Return Data</h2>
                <p className="mt-2 text-sm text-gray-600">Optional: Include tax return information for better accuracy</p>
              </div>

              <div className="space-y-4">
                <div className="flex items-center p-4 bg-blue-50 rounded-lg">
                  <input
                    type="checkbox"
                    checked={formData.include_tax_data}
                    onChange={(e) => setFormData({ ...formData, include_tax_data: e.target.checked })}
                    className="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label className="ml-3 text-sm font-medium text-gray-900">
                    Include tax return data (recommended for more accurate analysis)
                  </label>
                </div>

                {formData.include_tax_data && (
                  <div className="space-y-4 pt-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Gross Revenue ($)</label>
                        <input
                          type="number"
                          value={formData.gross_revenue === 0 ? '' : formData.gross_revenue}
                          onChange={(e) => {
                            const value = e.target.value === '' ? 0 : parseFloat(e.target.value);
                            setFormData({ ...formData, gross_revenue: value });
                          }}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="e.g., 540000"
                          min="0"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Total Expenses ($)</label>
                        <input
                          type="number"
                          value={formData.total_expenses === 0 ? '' : formData.total_expenses}
                          onChange={(e) => {
                            const value = e.target.value === '' ? 0 : parseFloat(e.target.value);
                            setFormData({ ...formData, total_expenses: value });
                          }}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="e.g., 420000"
                          min="0"
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Net Income ($)</label>
                        <input
                          type="number"
                          value={formData.net_income === 0 ? '' : formData.net_income}
                          onChange={(e) => {
                            const value = e.target.value === '' ? 0 : parseFloat(e.target.value);
                            setFormData({ ...formData, net_income: value });
                          }}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="e.g., 120000"
                          min="0"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Tax Year</label>
                        <input
                          type="number"
                          value={formData.tax_year}
                          onChange={(e) => setFormData({ ...formData, tax_year: parseInt(e.target.value) || 2024 })}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="2024"
                          min="2000"
                          max="2025"
                        />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Step 5: Review */}
          {currentStep === 5 && (
            <div className="space-y-6 animate-slide-in">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Review Your Application</h2>
                <p className="mt-2 text-sm text-gray-600">Please review all information before submitting</p>
              </div>

              <div className="space-y-4">
                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-900 mb-3">Business Information</h3>
                  <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                    <dt className="text-gray-600">Business Name:</dt>
                    <dd className="text-gray-900 font-medium">{formData.business_name}</dd>
                    <dt className="text-gray-600">Industry:</dt>
                    <dd className="text-gray-900 font-medium">{formData.industry}</dd>
                    <dt className="text-gray-600">Business Age:</dt>
                    <dd className="text-gray-900 font-medium">{formData.business_age_years} years</dd>
                  </dl>
                </div>

                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-900 mb-3">Loan Details</h3>
                  <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                    <dt className="text-gray-600">Loan Amount:</dt>
                    <dd className="text-gray-900 font-medium">${formData.loan_amount.toLocaleString()}</dd>
                    <dt className="text-gray-600">Term:</dt>
                    <dd className="text-gray-900 font-medium">{formData.term_months} months</dd>
                    <dt className="text-gray-600">Interest Rate:</dt>
                    <dd className="text-gray-900 font-medium">{(formData.annual_interest_rate * 100).toFixed(1)}%</dd>
                    <dt className="text-gray-600">Existing Debt:</dt>
                    <dd className="text-gray-900 font-medium">${formData.existing_debt.toLocaleString()}</dd>
                  </dl>
                </div>

                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-900 mb-3">Bank Statement Data</h3>
                  <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                    <dt className="text-gray-600">Months Covered:</dt>
                    <dd className="text-gray-900 font-medium">{formData.months_covered} months</dd>
                    <dt className="text-gray-600">NSF Fees:</dt>
                    <dd className="text-gray-900 font-medium">{formData.nsf_fees}</dd>
                    <dt className="text-gray-600">Average Balance:</dt>
                    <dd className="text-gray-900 font-medium">${formData.average_balance.toLocaleString()}</dd>
                  </dl>
                </div>

                {formData.include_tax_data && (
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-semibold text-gray-900 mb-3">Tax Return Data</h3>
                    <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                      <dt className="text-gray-600">Gross Revenue:</dt>
                      <dd className="text-gray-900 font-medium">${formData.gross_revenue.toLocaleString()}</dd>
                      <dt className="text-gray-600">Total Expenses:</dt>
                      <dd className="text-gray-900 font-medium">${formData.total_expenses.toLocaleString()}</dd>
                      <dt className="text-gray-600">Net Income:</dt>
                      <dd className="text-gray-900 font-medium">${formData.net_income.toLocaleString()}</dd>
                      <dt className="text-gray-600">Tax Year:</dt>
                      <dd className="text-gray-900 font-medium">{formData.tax_year}</dd>
                    </dl>
                  </div>
                )}
              </div>

              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-800">{error}</p>
                </div>
              )}

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-sm text-blue-800">
                  By submitting this application, you authorize our AI agents to analyze your financial data and generate a credit memo.
                </p>
              </div>
            </div>
          )}

          {/* Step 6: Results */}
          {currentStep === 6 && (
            <div className="space-y-6 animate-slide-in">
              {loading ? (
                <div className="text-center py-12">
                  <div className="inline-block h-16 w-16 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
                  <p className="mt-4 text-lg text-gray-600">Running multi-agent analysis...</p>
                  <p className="mt-2 text-sm text-gray-500">This may take a few seconds</p>
                </div>
              ) : result ? (
                <>
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900">Analysis Complete</h2>
                    <p className="mt-2 text-sm text-gray-600">Your loan application has been analyzed by our AI agents</p>
                  </div>

                  {/* Score & Recommendation */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg">
                      <p className="text-sm text-gray-600 mb-2">Underwriting Score</p>
                      <p className="text-5xl font-bold text-blue-900">{result.underwriting_score}<span className="text-2xl">/100</span></p>
                    </div>
                    <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-6 rounded-lg">
                      <p className="text-sm text-gray-600 mb-2">Recommendation</p>
                      <p className={`text-2xl font-bold px-4 py-2 rounded inline-block ${getRecommendationColor(result.recommendation)}`}>
                        {result.recommendation.replace(/_/g, ' ')}
                      </p>
                    </div>
                  </div>

                  {/* Risk Assessment */}
                  <div className="bg-white border border-gray-200 rounded-lg p-6">
                    <h3 className="text-lg font-semibold mb-4">Risk Assessment</h3>
                    <div className="mb-4">
                      <span className="text-sm text-gray-600">Risk Level: </span>
                      <span className={`px-4 py-2 rounded-lg font-medium ${getRiskColor(result.risk_assessment.risk_level)}`}>
                        {result.risk_assessment.risk_level}
                      </span>
                    </div>

                    {result.risk_assessment.flags.length > 0 && (
                      <div className="mb-4">
                        <p className="text-sm font-medium text-gray-700 mb-2">Risk Flags:</p>
                        <ul className="space-y-2">
                          {result.risk_assessment.flags.map((flag, idx) => (
                            <li key={idx} className="flex items-start">
                              <span className={`mr-2 px-2 py-1 rounded text-xs font-medium ${
                                flag.severity === 'HIGH' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'
                              }`}>
                                {flag.severity}
                              </span>
                              <span className="text-sm">{flag.message}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {result.risk_assessment.positive_signals.length > 0 && (
                      <div>
                        <p className="text-sm font-medium text-gray-700 mb-2">Positive Signals:</p>
                        <ul className="space-y-1">
                          {result.risk_assessment.positive_signals.map((signal, idx) => (
                            <li key={idx} className="text-sm text-green-700 flex items-center">
                              <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                              </svg>
                              {signal}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>

                  {/* Financial Metrics */}
                  <div className="bg-white border border-gray-200 rounded-lg p-6">
                    <h3 className="text-lg font-semibold mb-4">Financial Metrics</h3>
                    <div className="grid grid-cols-3 gap-4">
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-xs text-gray-600 mb-1">DSCR</p>
                        <p className="text-2xl font-bold text-gray-900">{result.financial_metrics.dscr.toFixed(2)}</p>
                      </div>
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-xs text-gray-600 mb-1">Stability Score</p>
                        <p className="text-2xl font-bold text-gray-900">{result.financial_metrics.stability_score}/100</p>
                      </div>
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-xs text-gray-600 mb-1">Revenue Volatility</p>
                        <p className="text-2xl font-bold text-gray-900">{(result.financial_metrics.revenue_volatility * 100).toFixed(1)}%</p>
                      </div>
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-xs text-gray-600 mb-1">Avg Monthly Revenue</p>
                        <p className="text-xl font-bold text-gray-900">${(result.financial_metrics.avg_monthly_revenue / 1000).toFixed(0)}K</p>
                      </div>
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-xs text-gray-600 mb-1">Monthly Cash Flow</p>
                        <p className="text-xl font-bold text-gray-900">${(result.financial_metrics.avg_monthly_cash_flow / 1000).toFixed(0)}K</p>
                      </div>
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-xs text-gray-600 mb-1">Debt-to-Revenue</p>
                        <p className="text-2xl font-bold text-gray-900">{(result.financial_metrics.debt_to_revenue * 100).toFixed(0)}%</p>
                      </div>
                    </div>
                  </div>

                  {/* Conditions */}
                  {result.conditions.length > 0 && (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
                      <h3 className="text-lg font-semibold text-yellow-900 mb-3">Approval Conditions</h3>
                      <ul className="list-disc list-inside space-y-1">
                        {result.conditions.map((condition, idx) => (
                          <li key={idx} className="text-sm text-yellow-800">{condition}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Credit Memo - Professional Document */}
                  <CreditMemoDocument
                    memo={result.credit_memo}
                    businessName={result.business_info.business_name}
                    loanAmount={result.business_info.loan_amount}
                    recommendation={result.recommendation}
                    underwritingScore={result.underwriting_score}
                  />
                </>
              ) : null}
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="mt-8 pt-6 border-t border-gray-200 flex justify-between">
            {currentStep > 1 && currentStep < 6 && (
              <button
                onClick={handleBack}
                className="px-6 py-3 border-2 border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 hover:border-gray-400 hover:shadow-md hover:-translate-y-0.5 transition-all duration-200"
              >
                Back
              </button>
            )}

            {currentStep < 5 && (
              <button
                onClick={handleNext}
                className="ml-auto px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg font-medium shadow-lg hover:shadow-xl hover:-translate-y-0.5 hover:from-blue-700 hover:to-blue-800 transition-all duration-200"
              >
                Continue
              </button>
            )}

            {currentStep === 5 && (
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="ml-auto px-8 py-3 bg-gradient-to-r from-green-600 to-green-700 text-white rounded-lg font-medium shadow-lg hover:shadow-xl hover:-translate-y-0.5 hover:from-green-700 hover:to-green-800 disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed disabled:shadow-none disabled:translate-y-0 transition-all duration-200"
              >
                {loading ? 'Analyzing...' : 'Submit & Analyze'}
              </button>
            )}

            {currentStep === 6 && result && (
              <button
                onClick={handleStartOver}
                className="ml-auto px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg font-medium shadow-lg hover:shadow-xl hover:-translate-y-0.5 hover:from-blue-700 hover:to-blue-800 transition-all duration-200"
              >
                Start New Application
              </button>
            )}
          </div>
        </div>
      </main>

      <footer className="bg-white/60 backdrop-blur-sm border-t border-gray-200/50 mt-12 py-8">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
            <div className="text-center md:text-left">
              <p className="text-sm font-semibold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Multi-Agent Kaaj AI Financial Analyzer
              </p>
              <p className="text-xs text-gray-500 mt-1">Built with FastAPI, OpenAI, React, and TailwindCSS</p>
            </div>
            <div className="flex items-center space-x-6 text-xs text-gray-500">
              <div className="flex items-center space-x-2">
                <svg className="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span>AI-Powered Analysis</span>
              </div>
              <div className="flex items-center space-x-2">
                <svg className="w-4 h-4 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                </svg>
                <span>Secure & Confidential</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
