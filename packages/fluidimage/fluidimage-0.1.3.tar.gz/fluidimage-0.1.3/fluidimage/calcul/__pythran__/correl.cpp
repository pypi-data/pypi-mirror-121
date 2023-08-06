#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/float32.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/float32.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/int_.hpp>
#include <pythonic/include/builtins/max.hpp>
#include <pythonic/include/builtins/min.hpp>
#include <pythonic/include/builtins/pythran/make_shape.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/empty.hpp>
#include <pythonic/include/numpy/float32.hpp>
#include <pythonic/include/numpy/sqrt.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/numpy/sum.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/floordiv.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/neg.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/int_.hpp>
#include <pythonic/builtins/max.hpp>
#include <pythonic/builtins/min.hpp>
#include <pythonic/builtins/pythran/make_shape.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/empty.hpp>
#include <pythonic/numpy/float32.hpp>
#include <pythonic/numpy/sqrt.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/numpy/sum.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/floordiv.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/neg.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_correl
{
  struct __transonic__
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef pythonic::types::str __type0;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type0>()))>::type result_type;
    }  ;
    inline
    typename type::result_type operator()() const;
    ;
  }  ;
  struct correl_numpy
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type3;
      typedef decltype(std::declval<__type2>()(std::declval<__type3>())) __type4;
      typedef long __type5;
      typedef decltype(pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type5>())) __type6;
      typedef decltype(pythonic::operator_::add(std::declval<__type6>(), std::declval<__type5>())) __type7;
      typedef typename pythonic::lazy<__type7>::type __type8;
      typedef decltype(std::declval<__type1>()(std::declval<__type8>(), std::declval<__type8>())) __type10;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float32{})>::type>::type __type11;
      typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type10>(), std::declval<__type11>()))>::type __type12;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type13;
      typedef decltype(pythonic::operator_::add(std::declval<__type3>(), std::declval<__type5>())) __type15;
      typedef decltype(std::declval<__type13>()(std::declval<__type15>())) __type16;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type16>::type::iterator>::value_type>::type __type17;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type17>(), std::declval<__type17>())) __type22;
      typedef indexable<__type22> __type23;
      typedef typename __combined<__type12,__type23>::type __type24;
      typedef decltype(std::declval<__type13>()(std::declval<__type3>())) __type27;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type27>::type::iterator>::value_type>::type __type28;
      typedef decltype(pythonic::operator_::add(std::declval<__type28>(), std::declval<__type3>())) __type30;
      typedef decltype(pythonic::operator_::add(std::declval<__type30>(), std::declval<__type5>())) __type31;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type17>(), std::declval<__type31>())) __type32;
      typedef indexable<__type32> __type33;
      typedef typename __combined<__type24,__type33>::type __type34;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type31>(), std::declval<__type17>())) __type45;
      typedef indexable<__type45> __type46;
      typedef typename __combined<__type34,__type46>::type __type47;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type31>(), std::declval<__type31>())) __type58;
      typedef indexable<__type58> __type59;
      typedef typename __combined<__type47,__type59>::type __type60;
      typedef typename pythonic::assignable<double>::type __type61;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type62;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type62>())) __type64;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type64>::type>::type>::type __type65;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::min{})>::type>::type __type66;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type67;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type67>())) __type68;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type68>::type>::type>::type __type69;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type69>(), std::declval<__type5>())) __type70;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type65>(), std::declval<__type5>())) __type72;
      typedef decltype(pythonic::operator_::sub(std::declval<__type70>(), std::declval<__type72>())) __type73;
      typedef decltype(pythonic::operator_::neg(std::declval<__type3>())) __type75;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type75>(), std::declval<__type17>()))>::type __type77;
      typedef decltype(pythonic::operator_::add(std::declval<__type73>(), std::declval<__type77>())) __type78;
      typedef decltype(std::declval<__type66>()(std::declval<__type78>(), std::declval<__type5>())) __type79;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type65>(), std::declval<__type79>()))>::type __type80;
      typedef decltype(std::declval<__type13>()(std::declval<__type80>())) __type81;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type81>::type::iterator>::value_type>::type __type82;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::neg(std::declval<__type79>()))>::type __type91;
      typedef decltype(pythonic::operator_::add(std::declval<__type82>(), std::declval<__type91>())) __type92;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type64>::type>::type>::type __type93;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type68>::type>::type>::type __type94;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type94>(), std::declval<__type5>())) __type95;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type93>(), std::declval<__type5>())) __type97;
      typedef decltype(pythonic::operator_::sub(std::declval<__type95>(), std::declval<__type97>())) __type98;
      typedef decltype(pythonic::operator_::add(std::declval<__type98>(), std::declval<__type77>())) __type103;
      typedef decltype(std::declval<__type66>()(std::declval<__type103>(), std::declval<__type5>())) __type104;
      typedef decltype(pythonic::operator_::add(std::declval<__type93>(), std::declval<__type104>())) __type105;
      typedef decltype(std::declval<__type13>()(std::declval<__type105>())) __type106;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type106>::type::iterator>::value_type>::type __type107;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::neg(std::declval<__type104>()))>::type __type116;
      typedef decltype(pythonic::operator_::add(std::declval<__type107>(), std::declval<__type116>())) __type117;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type92>(), std::declval<__type117>())) __type118;
      typedef decltype(std::declval<__type62>()[std::declval<__type118>()]) __type119;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::max{})>::type>::type __type121;
      typedef typename __combined<__type5,__type78>::type __type129;
      typedef typename pythonic::assignable<decltype(std::declval<__type121>()(std::declval<__type129>(), std::declval<__type78>()))>::type __type130;
      typedef decltype(pythonic::operator_::add(std::declval<__type130>(), std::declval<__type82>())) __type132;
      typedef typename __combined<__type5,__type103>::type __type140;
      typedef typename pythonic::assignable<decltype(std::declval<__type121>()(std::declval<__type140>(), std::declval<__type103>()))>::type __type141;
      typedef decltype(pythonic::operator_::add(std::declval<__type141>(), std::declval<__type107>())) __type143;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type132>(), std::declval<__type143>())) __type144;
      typedef decltype(std::declval<__type67>()[std::declval<__type144>()]) __type145;
      typedef decltype(pythonic::operator_::mul(std::declval<__type119>(), std::declval<__type145>())) __type146;
      typedef decltype(pythonic::operator_::add(std::declval<__type61>(), std::declval<__type146>())) __type147;
      typedef typename __combined<__type61,__type147>::type __type148;
      typedef typename __combined<__type148,__type146>::type __type149;
      typedef decltype(pythonic::operator_::add(std::declval<__type105>(), std::declval<__type93>())) __type150;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type95>(), std::declval<__type94>())) __type151;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type151>(), std::declval<__type5>())) __type152;
      typedef decltype(pythonic::operator_::sub(std::declval<__type98>(), std::declval<__type152>())) __type153;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type97>(), std::declval<__type93>())) __type154;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type154>(), std::declval<__type5>())) __type155;
      typedef decltype(pythonic::operator_::sub(std::declval<__type153>(), std::declval<__type155>())) __type156;
      typedef decltype(pythonic::operator_::add(std::declval<__type103>(), std::declval<__type156>())) __type157;
      typedef decltype(pythonic::operator_::add(std::declval<__type157>(), std::declval<__type77>())) __type158;
      typedef decltype(std::declval<__type66>()(std::declval<__type158>(), std::declval<__type5>())) __type159;
      typedef decltype(pythonic::operator_::add(std::declval<__type150>(), std::declval<__type159>())) __type160;
      typedef decltype(pythonic::operator_::mul(std::declval<__type160>(), std::declval<__type80>())) __type162;
      typedef decltype(pythonic::operator_::div(std::declval<__type149>(), std::declval<__type162>())) __type163;
      typedef container<typename std::remove_reference<__type163>::type> __type164;
      typedef decltype(pythonic::operator_::add(std::declval<__type95>(), std::declval<__type97>())) __type176;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type28>(), std::declval<__type5>()))>::type __type178;
      typedef decltype(pythonic::operator_::add(std::declval<__type176>(), std::declval<__type178>())) __type179;
      typedef decltype(pythonic::operator_::sub(std::declval<__type179>(), std::declval<__type94>())) __type181;
      typedef typename __combined<__type181,__type5>::type __type182;
      typedef decltype(std::declval<__type121>()(std::declval<__type182>(), std::declval<__type5>())) __type183;
      typedef decltype(pythonic::operator_::sub(std::declval<__type93>(), std::declval<__type183>())) __type184;
      typedef decltype(std::declval<__type13>()(std::declval<__type184>())) __type185;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type185>::type::iterator>::value_type>::type __type186;
      typedef decltype(pythonic::operator_::add(std::declval<__type186>(), std::declval<__type5>())) __type187;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type92>(), std::declval<__type187>())) __type188;
      typedef decltype(std::declval<__type62>()[std::declval<__type188>()]) __type189;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type98>(), std::declval<__type178>()))>::type __type200;
      typedef decltype(pythonic::operator_::add(std::declval<__type200>(), std::declval<__type186>())) __type202;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type132>(), std::declval<__type202>())) __type203;
      typedef decltype(std::declval<__type67>()[std::declval<__type203>()]) __type204;
      typedef decltype(pythonic::operator_::mul(std::declval<__type189>(), std::declval<__type204>())) __type205;
      typedef decltype(pythonic::operator_::add(std::declval<__type61>(), std::declval<__type205>())) __type206;
      typedef typename __combined<__type61,__type206>::type __type207;
      typedef typename __combined<__type207,__type205>::type __type208;
      typedef decltype(pythonic::operator_::sub(std::declval<__type184>(), std::declval<__type93>())) __type209;
      typedef decltype(pythonic::operator_::add(std::declval<__type176>(), std::declval<__type152>())) __type212;
      typedef decltype(pythonic::operator_::add(std::declval<__type212>(), std::declval<__type155>())) __type215;
      typedef decltype(pythonic::operator_::add(std::declval<__type179>(), std::declval<__type215>())) __type216;
      typedef decltype(pythonic::operator_::add(std::declval<__type216>(), std::declval<__type178>())) __type217;
      typedef decltype(pythonic::operator_::sub(std::declval<__type182>(), std::declval<__type217>())) __type218;
      typedef decltype(pythonic::operator_::sub(std::declval<__type218>(), std::declval<__type94>())) __type219;
      typedef typename __combined<__type219,__type5>::type __type220;
      typedef decltype(std::declval<__type121>()(std::declval<__type220>(), std::declval<__type5>())) __type221;
      typedef decltype(pythonic::operator_::sub(std::declval<__type209>(), std::declval<__type221>())) __type222;
      typedef decltype(pythonic::operator_::mul(std::declval<__type222>(), std::declval<__type80>())) __type224;
      typedef decltype(pythonic::operator_::div(std::declval<__type208>(), std::declval<__type224>())) __type225;
      typedef container<typename std::remove_reference<__type225>::type> __type226;
      typedef decltype(pythonic::operator_::add(std::declval<__type70>(), std::declval<__type72>())) __type233;
      typedef decltype(pythonic::operator_::add(std::declval<__type233>(), std::declval<__type178>())) __type236;
      typedef decltype(pythonic::operator_::sub(std::declval<__type236>(), std::declval<__type69>())) __type238;
      typedef typename __combined<__type238,__type5>::type __type239;
      typedef decltype(std::declval<__type121>()(std::declval<__type239>(), std::declval<__type5>())) __type240;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::sub(std::declval<__type65>(), std::declval<__type240>()))>::type __type241;
      typedef decltype(std::declval<__type13>()(std::declval<__type241>())) __type242;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type242>::type::iterator>::value_type>::type __type243;
      typedef decltype(pythonic::operator_::add(std::declval<__type243>(), std::declval<__type5>())) __type244;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type244>(), std::declval<__type117>())) __type270;
      typedef decltype(std::declval<__type62>()[std::declval<__type270>()]) __type271;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type73>(), std::declval<__type178>()))>::type __type279;
      typedef decltype(pythonic::operator_::add(std::declval<__type279>(), std::declval<__type243>())) __type281;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type281>(), std::declval<__type143>())) __type293;
      typedef decltype(std::declval<__type67>()[std::declval<__type293>()]) __type294;
      typedef decltype(pythonic::operator_::mul(std::declval<__type271>(), std::declval<__type294>())) __type295;
      typedef decltype(pythonic::operator_::add(std::declval<__type61>(), std::declval<__type295>())) __type296;
      typedef typename __combined<__type61,__type296>::type __type297;
      typedef typename __combined<__type297,__type295>::type __type298;
      typedef decltype(pythonic::operator_::mul(std::declval<__type160>(), std::declval<__type241>())) __type311;
      typedef decltype(pythonic::operator_::div(std::declval<__type298>(), std::declval<__type311>())) __type312;
      typedef container<typename std::remove_reference<__type312>::type> __type313;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type244>(), std::declval<__type187>())) __type336;
      typedef decltype(std::declval<__type62>()[std::declval<__type336>()]) __type337;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type281>(), std::declval<__type202>())) __type351;
      typedef decltype(std::declval<__type67>()[std::declval<__type351>()]) __type352;
      typedef decltype(pythonic::operator_::mul(std::declval<__type337>(), std::declval<__type352>())) __type353;
      typedef decltype(pythonic::operator_::add(std::declval<__type61>(), std::declval<__type353>())) __type354;
      typedef typename __combined<__type61,__type354>::type __type355;
      typedef typename __combined<__type355,__type353>::type __type356;
      typedef decltype(pythonic::operator_::mul(std::declval<__type222>(), std::declval<__type241>())) __type372;
      typedef decltype(pythonic::operator_::div(std::declval<__type356>(), std::declval<__type372>())) __type373;
      typedef container<typename std::remove_reference<__type373>::type> __type374;
      typedef typename __combined<__type60,__type164,__type23,__type226,__type33,__type313,__type46,__type374,__type59>::type __type375;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SIZE{}, std::declval<__type62>())) __type377;
      typedef decltype(pythonic::operator_::mul(std::declval<__type375>(), std::declval<__type377>())) __type378;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sqrt{})>::type>::type __type379;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type380;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type381;
      typedef decltype(std::declval<__type381>()(std::declval<__type62>())) __type383;
      typedef decltype(std::declval<__type380>()(std::declval<__type383>())) __type384;
      typedef decltype(std::declval<__type381>()(std::declval<__type67>())) __type386;
      typedef decltype(std::declval<__type380>()(std::declval<__type386>())) __type387;
      typedef decltype(pythonic::operator_::mul(std::declval<__type384>(), std::declval<__type387>())) __type388;
      typedef decltype(std::declval<__type379>()(std::declval<__type388>())) __type389;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type378>(), std::declval<__type389>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& im0, argument_type1&& im1, argument_type2&& disp_max) const
    ;
  }  ;
  inline
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.4.11"));
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename correl_numpy::type<argument_type0, argument_type1, argument_type2>::result_type correl_numpy::operator()(argument_type0&& im0, argument_type1&& im1, argument_type2&& disp_max) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type3;
    typedef decltype(std::declval<__type2>()(std::declval<__type3>())) __type4;
    typedef long __type5;
    typedef decltype(pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type5>())) __type6;
    typedef decltype(pythonic::operator_::add(std::declval<__type6>(), std::declval<__type5>())) __type7;
    typedef typename pythonic::lazy<__type7>::type __type8;
    typedef decltype(std::declval<__type1>()(std::declval<__type8>(), std::declval<__type8>())) __type10;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float32{})>::type>::type __type11;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type10>(), std::declval<__type11>()))>::type __type12;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type13;
    typedef decltype(pythonic::operator_::add(std::declval<__type3>(), std::declval<__type5>())) __type15;
    typedef decltype(std::declval<__type13>()(std::declval<__type15>())) __type16;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type16>::type::iterator>::value_type>::type __type17;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type17>(), std::declval<__type17>())) __type22;
    typedef indexable<__type22> __type23;
    typedef typename __combined<__type12,__type23>::type __type24;
    typedef decltype(std::declval<__type13>()(std::declval<__type3>())) __type27;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type27>::type::iterator>::value_type>::type __type28;
    typedef decltype(pythonic::operator_::add(std::declval<__type28>(), std::declval<__type3>())) __type30;
    typedef decltype(pythonic::operator_::add(std::declval<__type30>(), std::declval<__type5>())) __type31;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type17>(), std::declval<__type31>())) __type32;
    typedef indexable<__type32> __type33;
    typedef typename __combined<__type24,__type33>::type __type34;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type31>(), std::declval<__type17>())) __type45;
    typedef indexable<__type45> __type46;
    typedef typename __combined<__type34,__type46>::type __type47;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type31>(), std::declval<__type31>())) __type58;
    typedef indexable<__type58> __type59;
    typedef typename __combined<__type47,__type59>::type __type60;
    typedef typename pythonic::assignable<double>::type __type61;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type62;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type62>())) __type64;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type64>::type>::type>::type __type65;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::min{})>::type>::type __type66;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type67;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type67>())) __type68;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type68>::type>::type>::type __type69;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type69>(), std::declval<__type5>())) __type70;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type65>(), std::declval<__type5>())) __type72;
    typedef decltype(pythonic::operator_::sub(std::declval<__type70>(), std::declval<__type72>())) __type73;
    typedef decltype(pythonic::operator_::neg(std::declval<__type3>())) __type75;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type75>(), std::declval<__type17>()))>::type __type77;
    typedef decltype(pythonic::operator_::add(std::declval<__type73>(), std::declval<__type77>())) __type78;
    typedef decltype(std::declval<__type66>()(std::declval<__type78>(), std::declval<__type5>())) __type79;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type65>(), std::declval<__type79>()))>::type __type80;
    typedef decltype(std::declval<__type13>()(std::declval<__type80>())) __type81;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type81>::type::iterator>::value_type>::type __type82;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::neg(std::declval<__type79>()))>::type __type91;
    typedef decltype(pythonic::operator_::add(std::declval<__type82>(), std::declval<__type91>())) __type92;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type64>::type>::type>::type __type93;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type68>::type>::type>::type __type94;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type94>(), std::declval<__type5>())) __type95;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type93>(), std::declval<__type5>())) __type97;
    typedef decltype(pythonic::operator_::sub(std::declval<__type95>(), std::declval<__type97>())) __type98;
    typedef decltype(pythonic::operator_::add(std::declval<__type98>(), std::declval<__type77>())) __type103;
    typedef decltype(std::declval<__type66>()(std::declval<__type103>(), std::declval<__type5>())) __type104;
    typedef decltype(pythonic::operator_::add(std::declval<__type93>(), std::declval<__type104>())) __type105;
    typedef decltype(std::declval<__type13>()(std::declval<__type105>())) __type106;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type106>::type::iterator>::value_type>::type __type107;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::neg(std::declval<__type104>()))>::type __type116;
    typedef decltype(pythonic::operator_::add(std::declval<__type107>(), std::declval<__type116>())) __type117;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type92>(), std::declval<__type117>())) __type118;
    typedef decltype(std::declval<__type62>()[std::declval<__type118>()]) __type119;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::max{})>::type>::type __type121;
    typedef typename __combined<__type5,__type78>::type __type129;
    typedef typename pythonic::assignable<decltype(std::declval<__type121>()(std::declval<__type129>(), std::declval<__type78>()))>::type __type130;
    typedef decltype(pythonic::operator_::add(std::declval<__type130>(), std::declval<__type82>())) __type132;
    typedef typename __combined<__type5,__type103>::type __type140;
    typedef typename pythonic::assignable<decltype(std::declval<__type121>()(std::declval<__type140>(), std::declval<__type103>()))>::type __type141;
    typedef decltype(pythonic::operator_::add(std::declval<__type141>(), std::declval<__type107>())) __type143;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type132>(), std::declval<__type143>())) __type144;
    typedef decltype(std::declval<__type67>()[std::declval<__type144>()]) __type145;
    typedef decltype(pythonic::operator_::mul(std::declval<__type119>(), std::declval<__type145>())) __type146;
    typedef decltype(pythonic::operator_::add(std::declval<__type61>(), std::declval<__type146>())) __type147;
    typedef typename __combined<__type61,__type147>::type __type148;
    typedef typename __combined<__type148,__type146>::type __type149;
    typedef decltype(pythonic::operator_::add(std::declval<__type105>(), std::declval<__type93>())) __type150;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type95>(), std::declval<__type94>())) __type151;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type151>(), std::declval<__type5>())) __type152;
    typedef decltype(pythonic::operator_::sub(std::declval<__type98>(), std::declval<__type152>())) __type153;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type97>(), std::declval<__type93>())) __type154;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type154>(), std::declval<__type5>())) __type155;
    typedef decltype(pythonic::operator_::sub(std::declval<__type153>(), std::declval<__type155>())) __type156;
    typedef decltype(pythonic::operator_::add(std::declval<__type103>(), std::declval<__type156>())) __type157;
    typedef decltype(pythonic::operator_::add(std::declval<__type157>(), std::declval<__type77>())) __type158;
    typedef decltype(std::declval<__type66>()(std::declval<__type158>(), std::declval<__type5>())) __type159;
    typedef decltype(pythonic::operator_::add(std::declval<__type150>(), std::declval<__type159>())) __type160;
    typedef decltype(pythonic::operator_::mul(std::declval<__type160>(), std::declval<__type80>())) __type162;
    typedef decltype(pythonic::operator_::div(std::declval<__type149>(), std::declval<__type162>())) __type163;
    typedef container<typename std::remove_reference<__type163>::type> __type164;
    typedef decltype(pythonic::operator_::add(std::declval<__type95>(), std::declval<__type97>())) __type176;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type28>(), std::declval<__type5>()))>::type __type178;
    typedef decltype(pythonic::operator_::add(std::declval<__type176>(), std::declval<__type178>())) __type179;
    typedef decltype(pythonic::operator_::sub(std::declval<__type179>(), std::declval<__type94>())) __type181;
    typedef typename __combined<__type181,__type5>::type __type182;
    typedef decltype(std::declval<__type121>()(std::declval<__type182>(), std::declval<__type5>())) __type183;
    typedef decltype(pythonic::operator_::sub(std::declval<__type93>(), std::declval<__type183>())) __type184;
    typedef decltype(std::declval<__type13>()(std::declval<__type184>())) __type185;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type185>::type::iterator>::value_type>::type __type186;
    typedef decltype(pythonic::operator_::add(std::declval<__type186>(), std::declval<__type5>())) __type187;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type92>(), std::declval<__type187>())) __type188;
    typedef decltype(std::declval<__type62>()[std::declval<__type188>()]) __type189;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type98>(), std::declval<__type178>()))>::type __type200;
    typedef decltype(pythonic::operator_::add(std::declval<__type200>(), std::declval<__type186>())) __type202;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type132>(), std::declval<__type202>())) __type203;
    typedef decltype(std::declval<__type67>()[std::declval<__type203>()]) __type204;
    typedef decltype(pythonic::operator_::mul(std::declval<__type189>(), std::declval<__type204>())) __type205;
    typedef decltype(pythonic::operator_::add(std::declval<__type61>(), std::declval<__type205>())) __type206;
    typedef typename __combined<__type61,__type206>::type __type207;
    typedef typename __combined<__type207,__type205>::type __type208;
    typedef decltype(pythonic::operator_::sub(std::declval<__type184>(), std::declval<__type93>())) __type209;
    typedef decltype(pythonic::operator_::add(std::declval<__type176>(), std::declval<__type152>())) __type212;
    typedef decltype(pythonic::operator_::add(std::declval<__type212>(), std::declval<__type155>())) __type215;
    typedef decltype(pythonic::operator_::add(std::declval<__type179>(), std::declval<__type215>())) __type216;
    typedef decltype(pythonic::operator_::add(std::declval<__type216>(), std::declval<__type178>())) __type217;
    typedef decltype(pythonic::operator_::sub(std::declval<__type182>(), std::declval<__type217>())) __type218;
    typedef decltype(pythonic::operator_::sub(std::declval<__type218>(), std::declval<__type94>())) __type219;
    typedef typename __combined<__type219,__type5>::type __type220;
    typedef decltype(std::declval<__type121>()(std::declval<__type220>(), std::declval<__type5>())) __type221;
    typedef decltype(pythonic::operator_::sub(std::declval<__type209>(), std::declval<__type221>())) __type222;
    typedef decltype(pythonic::operator_::mul(std::declval<__type222>(), std::declval<__type80>())) __type224;
    typedef decltype(pythonic::operator_::div(std::declval<__type208>(), std::declval<__type224>())) __type225;
    typedef container<typename std::remove_reference<__type225>::type> __type226;
    typedef decltype(pythonic::operator_::add(std::declval<__type70>(), std::declval<__type72>())) __type233;
    typedef decltype(pythonic::operator_::add(std::declval<__type233>(), std::declval<__type178>())) __type236;
    typedef decltype(pythonic::operator_::sub(std::declval<__type236>(), std::declval<__type69>())) __type238;
    typedef typename __combined<__type238,__type5>::type __type239;
    typedef decltype(std::declval<__type121>()(std::declval<__type239>(), std::declval<__type5>())) __type240;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::sub(std::declval<__type65>(), std::declval<__type240>()))>::type __type241;
    typedef decltype(std::declval<__type13>()(std::declval<__type241>())) __type242;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type242>::type::iterator>::value_type>::type __type243;
    typedef decltype(pythonic::operator_::add(std::declval<__type243>(), std::declval<__type5>())) __type244;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type244>(), std::declval<__type117>())) __type270;
    typedef decltype(std::declval<__type62>()[std::declval<__type270>()]) __type271;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::add(std::declval<__type73>(), std::declval<__type178>()))>::type __type279;
    typedef decltype(pythonic::operator_::add(std::declval<__type279>(), std::declval<__type243>())) __type281;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type281>(), std::declval<__type143>())) __type293;
    typedef decltype(std::declval<__type67>()[std::declval<__type293>()]) __type294;
    typedef decltype(pythonic::operator_::mul(std::declval<__type271>(), std::declval<__type294>())) __type295;
    typedef decltype(pythonic::operator_::add(std::declval<__type61>(), std::declval<__type295>())) __type296;
    typedef typename __combined<__type61,__type296>::type __type297;
    typedef typename __combined<__type297,__type295>::type __type298;
    typedef decltype(pythonic::operator_::mul(std::declval<__type160>(), std::declval<__type241>())) __type311;
    typedef decltype(pythonic::operator_::div(std::declval<__type298>(), std::declval<__type311>())) __type312;
    typedef container<typename std::remove_reference<__type312>::type> __type313;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type244>(), std::declval<__type187>())) __type336;
    typedef decltype(std::declval<__type62>()[std::declval<__type336>()]) __type337;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type281>(), std::declval<__type202>())) __type351;
    typedef decltype(std::declval<__type67>()[std::declval<__type351>()]) __type352;
    typedef decltype(pythonic::operator_::mul(std::declval<__type337>(), std::declval<__type352>())) __type353;
    typedef decltype(pythonic::operator_::add(std::declval<__type61>(), std::declval<__type353>())) __type354;
    typedef typename __combined<__type61,__type354>::type __type355;
    typedef typename __combined<__type355,__type353>::type __type356;
    typedef decltype(pythonic::operator_::mul(std::declval<__type222>(), std::declval<__type241>())) __type372;
    typedef decltype(pythonic::operator_::div(std::declval<__type356>(), std::declval<__type372>())) __type373;
    typedef container<typename std::remove_reference<__type373>::type> __type374;
    typename pythonic::lazy<__type8>::type ny;
    typename pythonic::lazy<__type8>::type nx;
    ny= nx = pythonic::operator_::add(pythonic::operator_::mul(pythonic::builtins::functor::int_{}(disp_max), 2L), 1L);
    typename pythonic::assignable_noescape<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, im0)))>::type ny0 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, im0));
    typename pythonic::assignable_noescape<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, im0)))>::type nx0 = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, im0));
    typename pythonic::assignable_noescape<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, im1)))>::type ny1 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, im1));
    typename pythonic::assignable_noescape<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, im1)))>::type nx1 = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, im1));
    typename pythonic::assignable<typename __combined<__type60,__type164,__type23,__type226,__type33,__type313,__type46,__type374,__type59>::type>::type correl = pythonic::numpy::functor::empty{}(pythonic::builtins::pythran::functor::make_shape{}(ny, nx), pythonic::numpy::functor::float32{});
    {
      long  __target139893273763408 = pythonic::operator_::add(disp_max, 1L);
      for (long  xiy=0L; xiy < __target139893273763408; xiy += 1L)
      {
        typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(pythonic::operator_::neg(disp_max), xiy))>::type dispy = pythonic::operator_::add(pythonic::operator_::neg(disp_max), xiy);
        typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(ny1, pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(ny0, 2L), pythonic::operator_::functor::floordiv()(ny1, 2L)), dispy), 0L)))>::type nymax = pythonic::operator_::add(ny1, pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(ny0, 2L), pythonic::operator_::functor::floordiv()(ny1, 2L)), dispy), 0L));
        typename pythonic::assignable_noescape<decltype(pythonic::operator_::neg(pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(ny0, 2L), pythonic::operator_::functor::floordiv()(ny1, 2L)), dispy), 0L)))>::type ny1dep = pythonic::operator_::neg(pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(ny0, 2L), pythonic::operator_::functor::floordiv()(ny1, 2L)), dispy), 0L));
        typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::max{}(0L, pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(ny0, 2L), pythonic::operator_::functor::floordiv()(ny1, 2L)), dispy)))>::type ny0dep = pythonic::builtins::functor::max{}(0L, pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(ny0, 2L), pythonic::operator_::functor::floordiv()(ny1, 2L)), dispy));
        {
          long  __target139893277669600 = pythonic::operator_::add(disp_max, 1L);
          for (long  xix=0L; xix < __target139893277669600; xix += 1L)
          {
            typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(pythonic::operator_::neg(disp_max), xix))>::type dispx = pythonic::operator_::add(pythonic::operator_::neg(disp_max), xix);
            typename pythonic::assignable_noescape<decltype(pythonic::operator_::neg(pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx), 0L)))>::type nx1dep = pythonic::operator_::neg(pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx), 0L));
            typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::max{}(0L, pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx)))>::type nx0dep = pythonic::builtins::functor::max{}(0L, pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx));
            typename pythonic::assignable<typename __combined<__type148,__type146>::type>::type tmp = 0.0;
            {
              long  __target139893274870832 = nymax;
              for (long  iy=0L; iy < __target139893274870832; iy += 1L)
              {
                {
                  long  __target139893276510768 = pythonic::operator_::add(nx1, pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx), 0L));
                  for (long  ix=0L; ix < __target139893276510768; ix += 1L)
                  {
                    tmp += pythonic::operator_::mul(im1.fast(pythonic::types::make_tuple(pythonic::operator_::add(iy, ny1dep), pythonic::operator_::add(ix, nx1dep))), im0.fast(pythonic::types::make_tuple(pythonic::operator_::add(ny0dep, iy), pythonic::operator_::add(nx0dep, ix))));
                  }
                }
              }
            }
            correl.fast(pythonic::types::make_tuple(xiy, xix)) = pythonic::operator_::div(tmp, pythonic::operator_::mul(pythonic::operator_::add(nx1, pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx), 0L)), nymax));
          }
        }
        {
          long  __target139893277668736 = disp_max;
          for (long  xix_=0L; xix_ < __target139893277668736; xix_ += 1L)
          {
            typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(xix_, 1L))>::type dispx_ = pythonic::operator_::add(xix_, 1L);
            typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx_))>::type nx0dep_ = pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx_);
            typename pythonic::assignable<typename __combined<__type207,__type205>::type>::type tmp_ = 0.0;
            {
              long  __target139893276581168 = nymax;
              for (long  iy_=0L; iy_ < __target139893276581168; iy_ += 1L)
              {
                {
                  long  __target139893277618384 = pythonic::operator_::sub(nx1, pythonic::builtins::functor::max{}(pythonic::operator_::sub(pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx_), nx0), 0L));
                  for (long  ix_=0L; ix_ < __target139893277618384; ix_ += 1L)
                  {
                    tmp_ += pythonic::operator_::mul(im1.fast(pythonic::types::make_tuple(pythonic::operator_::add(iy_, ny1dep), pythonic::operator_::add(ix_, 0L))), im0[pythonic::types::make_tuple(pythonic::operator_::add(ny0dep, iy_), pythonic::operator_::add(nx0dep_, ix_))]);
                  }
                }
              }
            }
            correl[pythonic::types::make_tuple(xiy, pythonic::operator_::add(pythonic::operator_::add(xix_, disp_max), 1L))] = pythonic::operator_::div(tmp_, pythonic::operator_::mul(pythonic::operator_::sub(nx1, pythonic::builtins::functor::max{}(pythonic::operator_::sub(pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx_), nx0), 0L)), nymax));
          }
        }
      }
    }
    {
      long  __target139893273760144 = disp_max;
      for (long  xiy_=0L; xiy_ < __target139893273760144; xiy_ += 1L)
      {
        typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(xiy_, 1L))>::type dispy_ = pythonic::operator_::add(xiy_, 1L);
        typename pythonic::assignable_noescape<decltype(pythonic::operator_::sub(ny1, pythonic::builtins::functor::max{}(pythonic::operator_::sub(pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::functor::floordiv()(ny0, 2L), pythonic::operator_::functor::floordiv()(ny1, 2L)), dispy_), ny0), 0L)))>::type nymax_ = pythonic::operator_::sub(ny1, pythonic::builtins::functor::max{}(pythonic::operator_::sub(pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::functor::floordiv()(ny0, 2L), pythonic::operator_::functor::floordiv()(ny1, 2L)), dispy_), ny0), 0L));
        typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(ny0, 2L), pythonic::operator_::functor::floordiv()(ny1, 2L)), dispy_))>::type ny0dep_ = pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(ny0, 2L), pythonic::operator_::functor::floordiv()(ny1, 2L)), dispy_);
        {
          long  __target139893274940368 = pythonic::operator_::add(disp_max, 1L);
          for (long  xix__=0L; xix__ < __target139893274940368; xix__ += 1L)
          {
            typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(pythonic::operator_::neg(disp_max), xix__))>::type dispx__ = pythonic::operator_::add(pythonic::operator_::neg(disp_max), xix__);
            typename pythonic::assignable_noescape<decltype(pythonic::operator_::neg(pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx__), 0L)))>::type nx1dep__ = pythonic::operator_::neg(pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx__), 0L));
            typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::max{}(0L, pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx__)))>::type nx0dep__ = pythonic::builtins::functor::max{}(0L, pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx__));
            typename pythonic::assignable<typename __combined<__type297,__type295>::type>::type tmp__ = 0.0;
            {
              long  __target139893275434720 = nymax_;
              for (long  iy__=0L; iy__ < __target139893275434720; iy__ += 1L)
              {
                {
                  long  __target139893275009328 = pythonic::operator_::add(nx1, pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx__), 0L));
                  for (long  ix__=0L; ix__ < __target139893275009328; ix__ += 1L)
                  {
                    tmp__ += pythonic::operator_::mul(im1.fast(pythonic::types::make_tuple(pythonic::operator_::add(iy__, 0L), pythonic::operator_::add(ix__, nx1dep__))), im0[pythonic::types::make_tuple(pythonic::operator_::add(ny0dep_, iy__), pythonic::operator_::add(nx0dep__, ix__))]);
                  }
                }
              }
            }
            correl[pythonic::types::make_tuple(pythonic::operator_::add(pythonic::operator_::add(xiy_, disp_max), 1L), xix__)] = pythonic::operator_::div(tmp__, pythonic::operator_::mul(pythonic::operator_::add(nx1, pythonic::builtins::functor::min{}(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx__), 0L)), nymax_));
          }
        }
        {
          long  __target139893274941904 = disp_max;
          for (long  xix___=0L; xix___ < __target139893274941904; xix___ += 1L)
          {
            typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(xix___, 1L))>::type dispx___ = pythonic::operator_::add(xix___, 1L);
            typename pythonic::assignable_noescape<decltype(pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx___))>::type nx0dep___ = pythonic::operator_::add(pythonic::operator_::sub(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx___);
            typename pythonic::assignable<typename __combined<__type355,__type353>::type>::type tmp___ = 0.0;
            {
              long  __target139893276564976 = nymax_;
              for (long  iy___=0L; iy___ < __target139893276564976; iy___ += 1L)
              {
                {
                  long  __target139893276539104 = pythonic::operator_::sub(nx1, pythonic::builtins::functor::max{}(pythonic::operator_::sub(pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx___), nx0), 0L));
                  for (long  ix___=0L; ix___ < __target139893276539104; ix___ += 1L)
                  {
                    tmp___ += pythonic::operator_::mul(im1.fast(pythonic::types::make_tuple(pythonic::operator_::add(iy___, 0L), pythonic::operator_::add(ix___, 0L))), im0[pythonic::types::make_tuple(pythonic::operator_::add(ny0dep_, iy___), pythonic::operator_::add(nx0dep___, ix___))]);
                  }
                }
              }
            }
            correl[pythonic::types::make_tuple(pythonic::operator_::add(pythonic::operator_::add(xiy_, disp_max), 1L), pythonic::operator_::add(pythonic::operator_::add(xix___, disp_max), 1L))] = pythonic::operator_::div(tmp___, pythonic::operator_::mul(pythonic::operator_::sub(nx1, pythonic::builtins::functor::max{}(pythonic::operator_::sub(pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::functor::floordiv()(nx0, 2L), pythonic::operator_::functor::floordiv()(nx1, 2L)), dispx___), nx0), 0L)), nymax_));
          }
        }
      }
    }
    return pythonic::types::make_tuple(pythonic::operator_::mul(correl, pythonic::builtins::getattr(pythonic::types::attr::SIZE{}, im1)), pythonic::numpy::functor::sqrt{}(pythonic::operator_::mul(pythonic::numpy::functor::sum{}(pythonic::numpy::functor::square{}(im1)), pythonic::numpy::functor::sum{}(pythonic::numpy::functor::square{}(im0)))));
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_correl::__transonic__()());
inline
typename __pythran_correl::correl_numpy::type<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>, long>::result_type correl_numpy0(pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>&& im0, pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>&& im1, long&& disp_max) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_correl::correl_numpy()(im0, im1, disp_max);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran_correl::correl_numpy::type<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>, long>::result_type correl_numpy1(pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>&& im0, pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>&& im1, long&& disp_max) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_correl::correl_numpy()(im0, im1, disp_max);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran_correl::correl_numpy::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>, pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>, long>::result_type correl_numpy2(pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>&& im0, pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>&& im1, long&& disp_max) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_correl::correl_numpy()(im0, im1, disp_max);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran_correl::correl_numpy::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>, long>::result_type correl_numpy3(pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>&& im0, pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>&& im1, long&& disp_max) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_correl::correl_numpy()(im0, im1, disp_max);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_correl_numpy0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"im0", "im1", "disp_max",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(correl_numpy0(from_python<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_correl_numpy1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"im0", "im1", "disp_max",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(correl_numpy1(from_python<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_correl_numpy2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"im0", "im1", "disp_max",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(correl_numpy2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_correl_numpy3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"im0", "im1", "disp_max",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(correl_numpy3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_correl_numpy(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_correl_numpy0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_correl_numpy1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_correl_numpy2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_correl_numpy3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "correl_numpy", "\n""    - correl_numpy(float32[:,:], float32[:,:], int)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "correl_numpy",
    (PyCFunction)__pythran_wrapall_correl_numpy,
    METH_VARARGS | METH_KEYWORDS,
    "Correlations by hand using only numpy.\n""\n""    Supported prototypes:\n""\n""    - correl_numpy(float32[:,:], float32[:,:], int)\n""\n""    Parameters\n""    ----------\n""\n""    im0, im1 : images\n""      input images : 2D matrix\n""\n""    disp_max : int\n""      displacement max.\n""\n""    Notes\n""    -------\n""\n""    im1_shape inf to im0_shape\n""\n""    Returns\n""    -------\n""\n""    the computing correlation (size of computed correlation = disp_max*2 + 1)\n""\n"""},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "correl",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(correl)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(correl)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("correl",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.10.0",
                                      "2021-09-24 23:15:25.107192",
                                      "5e17ab3d26350f9669db09c0b4a82d3ac0a6dae91f3c5166137adff870f23a8d");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);

    PyModule_AddObject(theModule, "__transonic__", __transonic__);
    PYTHRAN_RETURN;
}

#endif