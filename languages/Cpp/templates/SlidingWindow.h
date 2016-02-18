#ifndef DEF_H_SLIDING_WINDOW_
#define DEF_H_SLIDING_WINDOW_

#include <deque>

/*
    T must define an operator=, an operator*(double) and an operator+(T)
*/

template<typename T>
class SlidingWindowMean
{
private:
    T mean_;
    int windowSize_;
    std::deque<T> memory_;

public:
    SlidingWindowMean(int windowSize = 15) : mean_(), windowSize_(windowSize), memory_() {}

    void push(const T& value) {
        const unsigned int memSize = memory_.size();
        if (memSize == windowSize_)
            memory_.pop_front();
        memory_.push_back(value);
        // Mean update
        mean_ = T();
        for (unsigned int i = 0; i < memSize; ++i)
            mean_ = mean_ + memory_[i];
        mean_ = mean_ * (1.0 / memSize);
    }

    T mean() { return mean_; }
};

template<typename T>
class SlidingWindowExp
{
private:
    T mean_;
    int nbValues_;
    double alpha_;

public:
    SlidingWindowExp(double alpha = 0.7) : mean_(), nbValues_(0), alpha_(alpha) {}

    void push(const T& value) {
        mean_ = mean_ * (1 - alpha_) + value * alpha_;
    }

    T mean() { return mean_; }
};

template<typename T>
class SlidingWindowNone
{
private:
    T mean_;

public:
    SlidingWindowNone() : mean_() {}

    void push(const T& value) {
        mean_ = value;
    }

    T mean() { return mean_; }
};

#ifdef USE_SLIDING_WINDOW_EXP
#define SlidingWindow SlidingWindowMean
#else
#ifdef USE_SLIDING_WINDOW_MEAN
#define SlidingWindow SlidingWindowExp
#else
#define SlidingWindow SlidingWindowNone
#endif
#endif


#endif //DEF_H_SLIDING_WINDOW_
