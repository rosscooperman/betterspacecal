Betterspacecal::Application.routes.draw do
  resources :observations, only: [ :index ] do
    collection { get :export }
  end
  root to: 'observations#index'
end
