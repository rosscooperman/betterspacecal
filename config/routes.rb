Betterspacecal::Application.routes.draw do
  resources :observations, only: [ :index ]
  root to: 'observations#index'
end
