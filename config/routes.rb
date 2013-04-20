Betterspacecal::Application.routes.draw do
  resources :satellites, only: [ :index ]
  root to: 'satellites#index'
end
